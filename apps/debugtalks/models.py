from django.db import models


class DebugTalks(models.Model):
    """
    调试模型类
    """
    id = models.AutoField(verbose_name="ID", primary_key=True, help_text="ID")
    name = models.CharField(verbose_name="debugtalk文件名称", max_length=200, default="debugtalk.py",
                            help_text="debugtalk文件名称", )
    debugtalk = models.TextField(null=True, default="#debugtalk.py", help_text="debugtalk.py文件")
    project = models.OneToOneField("projects.Projects", on_delete=models.CASCADE, related_name="debugtalks",
                                   help_text="所属项目")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_debugtalks"
        verbose_name = "debugtalks.py文件"

    def __str__(self):
        return self.name
