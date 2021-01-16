from django.db import models


class Interfaces(models.Model):
    """
    接口模型类
    """
    id = models.AutoField(verbose_name="接口ID", primary_key=True, help_text="接口ID")
    name = models.CharField(verbose_name="接口名称", help_text="接口名称", unique=True, max_length=200)
    tester = models.CharField(verbose_name="测试人员", help_text="测试人员", max_length=50)
    desc = models.CharField(verbose_name="接口描述", help_text="接口描述",
                            max_length=200, default="", blank=True, null=True)
    # 外建关联，级联操作，related_name是指定父表对子表引用名，如不指定，默认为子表模型类名小写_set(interface_set)
    project = models.ForeignKey(to="projects.Projects", on_delete=models.CASCADE, related_name="interface",
                                help_text="所属项目")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        db_table = "tb_interfaces"
        verbose_name = "接口"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 在打印模型类对象时，会自动调用
        return self.name
