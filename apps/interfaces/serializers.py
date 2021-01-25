from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from testcases.models import Testcases
from configures.models import Configures
from utils import handle_validates


class InterfacesModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id')

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S',
            }
        }

    # to_internal_value方法为反序列化输入的入口方法
    def to_internal_value(self, data):
        temp = super().to_internal_value(data)
        temp['project'] = temp.pop('project_id')
        return temp

    # to_representation方法为序列化输出的入口方法
    # def to_representation(self, instance):
    #     super().to_representation(instance)
    #     pass

    # def create(self, validated_data):
    #     project = validated_data.pop('project_id')
    #     validated_data['project'] = project
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     if 'project_id' in validated_data:
    #         project = validated_data.pop('project_id')
    #         validated_data['project'] = project
    #
    #     return super().update(instance, validated_data)


class TestcasesNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
    testcases = TestcasesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('testcases', )


class ConfiguresNamesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfaceIdModelSerializer(serializers.ModelSerializer):
    configures = ConfiguresNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('configures', )


class InterfaceRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[handle_validates.is_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')
