from rest_framework import serializers

from utils import handle_validates
from .models import Projects
from debugtalks.models import DebugTalks
from interfaces.models import Interfaces


class ProjectModelSerializer(serializers.ModelSerializer):
    """
    项目模型序列化器
    """

    class Meta:
        model = Projects
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S',  # 格式化输出日期格式
            }
        }

    def create(self, validated_data):
        project = super().create(validated_data)
        # 创建一条debug talk数据
        # DebugTalks.objects.create(project=project)
        DebugTalks.objects.create(project_id=project.id)
        return project


class ProjectNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('name', 'id')


class InterfaceNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class InterfacesSerializer(serializers.ModelSerializer):
    interfaces = InterfaceNamesSerializer(label='项目所属接口信息', help_text='项目所属接口信息',
                                          many=True)

    class Meta:
        model = Projects
        fields = ('interfaces',)


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID',
                                      write_only=True, validators=[handle_validates.is_existed_env_id])

    class Meta:
        model = Projects
        fields = ('id', 'env_id')
