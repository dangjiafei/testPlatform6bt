from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码', help_text='确认密码',
                                             min_length=6, max_length=20,
                                             write_only=True,
                                             error_messages={
                                                 'min_length': '请输入6-20位的确认密码',
                                                 'max_length': '请输入6-20位的确认密码', })

    token = serializers.CharField(label='token值', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '请输入6-20位的用户名',
                    'max_length': '请输入6-20位的用户名',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only': True,
                'required': True,
                # 添加邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')],
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '请输入6-20位的密码',
                    'max_length': '请输入6-20位的密码',
                }
            }
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('密码与确认密码不一致')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        # 创建user模型对象
        user = User.objects.create_user(**validated_data)

        # 创建token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
