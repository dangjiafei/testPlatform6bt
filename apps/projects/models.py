from django.db import models


class Projects(models.Model):
    """
    项目模型类
    """
    id = models.AutoField(verbose_name="项目ID", primary_key=True, help_text="项目ID")
    name = models.CharField(verbose_name="项目名称", help_text="项目名称", unique=True, max_length=200)
    leader = models.CharField(verbose_name="项目负责人", help_text="项目负责人", max_length=50)
    tester = models.CharField(verbose_name="测试人员", help_text="测试人员", max_length=50)
    programmer = models.CharField(verbose_name="开发人员", help_text="开发人员", max_length=50)
    publish_app = models.CharField(verbose_name="发布应用", help_text="发布应用", max_length=100)
    # blank=True用于设置在创建项目时, 前端可以不用传此字段, null=True用于设置数据库此字段可以为空, 一般是一起用
    desc = models.CharField(verbose_name="项目描述", help_text="项目描述",
                            max_length=200, default="", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_projects"
        verbose_name = "项目"

    def __str__(self):
        return self.name
