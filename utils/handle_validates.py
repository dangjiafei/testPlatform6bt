from django.db.models import QuerySet
from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs


def is_existed_project_id(value_id):
    qs = Projects.objects.filter(id=value_id)  # type: QuerySet
    if not qs.exists():
        raise serializers.ValidationError("项目id不存在")


def is_existed_interface_id(value_id):
    qs = Interfaces.objects.filter(id=value_id)  # type: QuerySet
    if not qs.exists():
        raise serializers.ValidationError("接口id不存在")


def is_existed_env_id(value_id):
    qs = Envs.objects.filter(id=value_id)  # type: QuerySet
    if not qs.exists():
        raise serializers.ValidationError("环境变量id不存在")
