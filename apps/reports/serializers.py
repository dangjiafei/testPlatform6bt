from rest_framework import serializers
from .models import Reports


class ReportModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y年%m月%d日 %H:%M:%S',
            }
        }

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['result'] = "Pass" if res['result'] else "Fail"
        return res


