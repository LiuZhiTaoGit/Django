from django.db import models

# Create your models here.

class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    def __str__(self):
        return self.username
class Task(models.Model):
    """任务"""
    level_choice = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
    )
    level = models.SmallIntegerField(verbose_name="程度",choices=level_choice,default=3)
    title = models.CharField(verbose_name="题目",max_length=64)
    detail = models.TextField(verbose_name="细节")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题", max_length=32)
    def __str__(self):
        return self.title


class PretyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空,null = True,  blank = True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级别"),
        (2, "2级别"),
        (3, "3级别"),
        (4, "4级别"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices, default=1)

    status_choices = (
        (1,"已经占用"),
        (2,"未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices, default=2)




class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")
    #无约束的
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1、 有约束
    #     to ，与这张表有关联
    #     to_filed, 表的一列
    # 2、 django自动
    #     写的depart
    #     生成数据列depart_id
    # 3、 部门表被删除
    #     3.1 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete = models.CASCADE)
            # 3.2 置空
    # depart  = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    #在django中做约束，对性别
    gender_choice = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="商品名",max_length=64)
    price = models.CharField(verbose_name="价格",max_length=64)
    status_choice = (
        (1,"待支付"),
        (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="支付状态",choices=status_choice)
    admin = models.ForeignKey(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)
