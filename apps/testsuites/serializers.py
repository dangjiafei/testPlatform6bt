import re

from rest_framework import serializers
from .models import Testsuites
from projects.models import Projects
from interfaces.models import Interfaces
from utils import handle_validates


def validate_include(value):
    """
    校验包含的接口是否为列表以及接口是否存在
    :param value: include
    :return:
    """
    obj = re.match(r'^\[\d+(, *\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式有误')

    result = obj.group()
    try:
        data = eval(result)
    except Exception as e:
        raise serializers.ValidationError('参数格式有误')

    for item in data:
        if not Interfaces.objects.filter(id=item).exists():
            raise serializers.ValidationError(f'接口id[{item}]不存在')


class TestsuitesModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuites
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S',
            },
            'update_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S',
            },
            'include': {
                'validators': [validate_include]
            }
        }

    # to_internal_value方法为反序列化输入的入口方法
    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project'] = tmp.pop('project_id')
        return tmp

    # def create(self, validated_data):
    #     project = validated_data.pop('project_id')
    #     validated_data['project'] = project
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     if 'project_id' in validated_data:
    #         project = validated_data.pop('project_id')
    #         validated_data['project'] = project
    #         return super().update(instance, validated_data)


class TestsuitesRunSerializer(serializers.ModelSerializer):
    """
    通过套件来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[handle_validates.is_existed_env_id])

    class Meta:
        model = Testsuites
        fields = ('id', 'env_id')
