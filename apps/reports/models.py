from django.db import models


class Reports(models.Model):
    """
    测试报告模型类
    """
    id = models.AutoField(verbose_name="报告ID", primary_key=True, help_text="报告ID")
    name = models.CharField(verbose_name="报告名称", max_length=200, unique=True, help_text="报告名称")
    result = models.BooleanField(verbose_name="执行结果", default=1, help_text="执行结果")  # 1为成功，0为失败
    count = models.IntegerField(verbose_name="用例总数", help_text="用例总数")
    success = models.IntegerField(verbose_name="成功总数", help_text="成功总数")
    html = models.TextField(verbose_name="报告HTML源码", help_text="报告HTML源码", null=True, blank=True, default="")
    summary = models.TextField(verbose_name="报告详情", help_text="报告详情", null=True, blank=True, default="")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_reports"
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
