from django.db import models


class Testsuites(models.Model):
    """
    测试套件模型类
    """
    id = models.AutoField(verbose_name="套件ID", primary_key=True, help_text="套件ID")
    name = models.CharField(verbose_name="配置名称", help_text="配置名称", max_length=50)
    project = models.ForeignKey("projects.Projects", on_delete=models.CASCADE, related_name="testsuites",
                                help_text="所属项目")
    include = models.TextField("包含的接口", null=False, help_text="包含的接口")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_testsuites"
        verbose_name = "套件信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
