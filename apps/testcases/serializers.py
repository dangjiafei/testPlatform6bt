from rest_framework import serializers

from projects.models import Projects
from testcases.models import Testcases
from interfaces.models import Interfaces
from envs.models import Envs
from utils import handle_validates


# 1、list: 显示项目名称、接口名称、用例名、用例的author
# 2、create: 项目id、接口id、request
# 3、retrieve：include、所选择的项目id、接口id、用例名、用例的author
class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id',
                                   write_only=True, validators=[handle_validates.is_existed_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id',
                                   write_only=True, validators=[handle_validates.is_existed_interface_id])

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'pid', 'iid',)

        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')
        return attrs


class TestcaseModelSerailizer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口信息', help_text='所属项目和接口信息')

    class Meta:
        model = Testcases
        exclude = ('update_time', 'create_time')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.pop('interface').get('iid')
        result['interface_id'] = iid
        return result

    def to_representation(self, instance):
        # instance.pop('include')
        result = super().to_representation(instance)
        result.pop('include')
        return result


class TestcaseRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[handle_validates.is_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')
