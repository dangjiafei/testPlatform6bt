import os
import json

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http.response import StreamingHttpResponse
from django.conf import settings
from django.utils.encoding import escape_uri_path

from . import serializers
from .models import Reports
from .utils import get_file_content


class ReportsViewset(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = serializers.ReportModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            response.data['summary'] = json.loads(response.data['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 1、从数据库中读取测试报告的HTML源码
        instance = self.get_object()

        # 2、将源码写入到html文件中
        # 获取测试报告的存放路径
        report_dir = settings.REPORT_DIR
        # 生成测试报告的完整路径
        report_full_dir = os.path.join(report_dir, instance.name + '.html')
        # 如果测试报告在reports目录下不存在，那么才生成HTML报告文件
        if not os.path.exists(report_full_dir):
            with open(report_full_dir, 'w') as file:
                file.write(instance.html)

        # 3、读写html文件对象，将其传递给StreamingHttpResponse
        # 第一个参数需要传递生成器对象（每次迭代需要返回文件数据）
        # 字符串 --> 字节类型
        # str.encode('utf-8')
        # 字节类型 --> 字符串
        # byte.decode('utf-8')

        # one_file_byte = instance.html.encode()
        one_file_byte = instance.html
        # response = StreamingHttpResponse(get_file_content(report_full_dir))
        response = StreamingHttpResponse(iter(one_file_byte))

        # 如果要提供用户下载，必须添加相关的响应头
        # Content-Type
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition
        # response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name}"
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{escape_uri_path(instance.name)}"
        return response

