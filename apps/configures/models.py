from django.db import models


class Configures(models.Model):
    """
    配置信息模型类
    """
    id = models.AutoField(verbose_name="配置ID", primary_key=True, help_text="配置ID")
    name = models.CharField(verbose_name="配置名称", help_text="配置名称", max_length=50)
    interface = models.ForeignKey("interfaces.Interfaces", on_delete=models.CASCADE, related_name="configures",
                                  help_text="所属接口")
    author = models.CharField(verbose_name="编写人员", max_length=50, help_text="编写人员")
    request = models.TextField(verbose_name="请求信息", help_text="请求信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_configures"
        verbose_name = "配置信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
