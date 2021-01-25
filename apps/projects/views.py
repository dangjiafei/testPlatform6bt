import json
import logging
import os
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Projects
from .serializers import ProjectModelSerializer, ProjectNamesSerializer, InterfacesSerializer, ProjectsRunSerializer
from interfaces.models import Interfaces
from configures.models import Configures
from envs.models import Envs
from testcases.models import Testcases
from testsuites.models import Testsuites
from utils import common


class ProjectViewSet(viewsets.ModelViewSet):
    """
    create:
        创建项目
    list:
        获取项目列表数据
    retrieve:
        获取项目详情接口
    names:
        获取所有项目名称接口
    interfaces:
        获取某个项目下的所有接口信息
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']

        for item in results:

            # 获取当前项目下的所有接口总数
            # item['interfaces'] = Interfaces.objects.filter(project_id=item.get('id')).count()

            # 获取当前项目下的所有套件总数
            item['testsuites'] = Testsuites.objects.filter(project_id=item.get('id')).count()
            """
            获取用例总数
            a.使用annotate方法来进行分组运算
            b.annotate方法可以传递聚合运算对象
            c.聚合运算会默认设置字段别名，testcases__count
            d.可以给聚合运算设置别名，别名=聚合运算对象
            e.values方法指定需要查询的字段
            """
            interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(
                project_id=item.get('id'))

            # 获取当前项目下的所有接口总数
            item['interfaces'] = interface_testcase_qs.count()

            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')

            item['testcases'] = testcases_count

            interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(
                project_id=item.get('id'))

            configures_count = 0
            for one_dict in interface_configure_qs:
                configures_count += one_dict.get('configures')
            item['configures'] = configures_count
        return response

    @action(methods=['GET', 'POST'], detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)

        interface_qs = Interfaces.objects.filter(project=instance)
        if not interface_qs.exists():
            data = {
                'ret': False,
                'msg': '此项目下无接口，无法运行'
            }
            return Response(data, status=400)

        runnable_testcase_obj = []
        for interface_obj in interface_qs:
            # 当前接口项目的用例所在查询集对象
            testcase_qs = Testcases.objects.filter(interface=interface_obj)
            if testcase_qs.exists():
                # 将两个列表合并
                runnable_testcase_obj.extend(list(testcase_qs))

        if len(runnable_testcase_obj) == 0:
            data = {
                'ret': False,
                'msg': '此项目下无用例，无法运行'
            }
            return Response(data, status=400)

        for testcase_obj in runnable_testcase_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 运行用例（生成报告）
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        a.不过当前类视图中，使用了多个不同的序列化器类，
        b.那么可以将get_serializer_class重写
        :return:
        """
        # c.继承视图集类之后，会提供action属性，指定当前请求的action方法名称
        # d.可以根据不同的action去选择不同的序列化器类（不同的查询集）
        if self.action == 'names':
            return ProjectNamesSerializer
        elif self.action == 'interfaces':
            return InterfacesSerializer
        elif self.action == 'run':
            return ProjectsRunSerializer
        else:
            return self.serializer_class

    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data['interfaces']
        return response

    def filter_queryset(self, queryset):
        if self.action == "names":
            return queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == "names":
            return None
        else:
            return super().paginate_queryset(queryset)
