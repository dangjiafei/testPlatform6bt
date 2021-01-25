from django.db import models


class Testcases(models.Model):
    """
    用例模型类
    """
    id = models.AutoField(verbose_name="用例ID", primary_key=True, help_text="用例ID")
    name = models.CharField(verbose_name="用例名称", help_text="用例名称", unique=True, max_length=200)
    interface = models.ForeignKey("interfaces.Interfaces", on_delete=models.CASCADE, help_text="所属接口",
                                  related_name="testcases")
    include = models.TextField(verbose_name="用例执行前置顺序", null=True, help_text="用例执行前置顺序")
    author = models.CharField(verbose_name="编写人员", max_length=50, help_text="编写人员")
    request = models.TextField(verbose_name="请求信息", help_text="请求信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_testcases"
        verbose_name = "用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
