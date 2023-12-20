from app import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from ..utils.pagination import Pagination
from ..utils.bootstrap import BootStrapModelForm
from django.utils.safestring import mark_safe
import os
import sys
# Create your views here.





def user_add(request):
    if request.method =="GET":
        context = {
            "gender_list": models.UserInfo.gender_choice,
            "depart_list":models.Department.objects.all()
        }
        return render(request, "user_add.html",context)
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    ac = request.POST.get("ac")
    datee = request.POST.get("datee")
    gen = request.POST.get("gen")
    dp = request.POST.get("dp")
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=ac, create_time=datee, depart_id=dp, gender=gen)
    return redirect("/user/list")

class UserModelForm(BootStrapModelForm):
    #新的验证
    name = forms.CharField(min_length=3, label="yonghuming")

    #定义样式
    # name = forms.CharField(
    #     min_length=3,
    #     label="yonghuming",
    #     widget=forms.TextInput(attrs={"class":"form-control"})
    # )


    ##1、默认的校验是不能为空，如果要加新的验证，在上面写
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]
        #添加样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class":"form-control"})
        #     "password": forms.TextInput(attrs={"class":"form-control"})
        # }
        #循环找到所有的插件

    ### 添加样式  有问题，不管之前有没有样式，都给他强制统一了，因此可以i优化。
    #如果之前有属性，就保留，如果没有，才添加
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args,**kwargs)
    #     for name,field in self.fields.items():
    #         if name=="password":
    #             continue
    #         field.widget.attrs = {"class":"form-control", "placeholder":field.label}

def user_model_form_add(request):
    if request.method=="GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form":form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'name': 'fdf', 'password': 'fdf', 'age': 3, 'account': Decimal('545'),
        #  'create_time': datetime.datetime(2025, 8, 7, 0, 0, tzinfo=backports.zoneinfo.ZoneInfo(key='UTC')), 'depart'
        #  : < Department: 策划 >, 'gender': 2}
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form":form})

def user_edit(request,nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
    #根据id去数据库获取要编辑的哪一行
        form = UserModelForm(instance=row_object)
        return render(request,"user_edit.html",{"form":form})
    # row_object = models.UserInfo.objects.filter(id=nid).first()
    #不知道用的数据，所以要先获取
    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #保存某个特定的值，除了表的
        # form.instance.password = jklfdfdj
        form.save()#保存数据
        return redirect('/user/list/')
    return render(request, 'user_edit.html',{"form":form})

def delete_user(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")

def user_list(request):
    """用户管理"""
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset,page_size=2)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    # for i in queryset:
    #     print(i.id,i.name,i.age, i.account, i.create_time.strftime("%Y-%m-%d"), i.get_gender_display(), i.depart.title)
    return render(request, "user_list.html",context)





