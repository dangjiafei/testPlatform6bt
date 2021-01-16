from django.db import models


class Envs(models.Model):
    """
    环境模型类
    """
    id = models.AutoField(verbose_name="ID", primary_key=True, help_text="ID")
    name = models.CharField(verbose_name="环境名称", max_length=200, unique=True, help_text="环境名称")
    base_url = models.URLField(verbose_name="请求base_url", max_length=200, help_text="请求base_url")
    desc = models.CharField(verbose_name="简要描述", max_length=200, help_text="简要描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_envs"
        verbose_name = "环境信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
