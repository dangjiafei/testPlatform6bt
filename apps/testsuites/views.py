import os
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Testsuites
from .serializers import TestsuitesModelSerializer, TestsuitesRunSerializer
from envs.models import Envs
from testcases.models import Testcases
from utils import common
from .utils import get_testcases_by_interface_ids


class TestsuitesViewSet(ModelViewSet):
    queryset = Testsuites.objects.all()
    serializer_class = TestsuitesModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=True)
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

        include = eval(instance.include)
        if len(include) == 0:
            data = {
                'ret': False,
                'msg': '此套件下未添加接口, 无法运行'
            }
            return Response(data, status=400)

        # 将include中的接口id转化为此接口下的用例id
        include = get_testcases_by_interface_ids(include)
        for testcase_id in include:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            if testcase_obj:
                common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        return TestsuitesRunSerializer if self.action == 'run' else self.serializer_class
