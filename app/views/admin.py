from app import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from ..utils.pagination import Pagination
from ..utils.bootstrap import BootStrapModelForm

from app.utils.encrypt import md5
from django.utils.safestring import mark_safe
import os
import sys
# Create your views here.

def admin_list(request):
    """管理员列表"""
    #检查用户是否已经登录，如果登录了才可以展示，如果没登录，跳回登录页面
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    # print(info)
    # {'id': 1, 'name': 'root'}
    # [19 / Oct / 2023 21: 25:36] "GET /admin/list/ HTTP/1.1"    200    9768
    # None

    #构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data
    #根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    #分页
    # queryset = models.Admin.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(), # 生成页码
        "search_data":search_data
    }

    # for i in queryset:
    #     print(i.id,i.name,i.age, i.account, i.create_time.strftime("%Y-%m-%d"), i.get_gender_display(), i.depart.title)
    return render(request, "admin_list.html", context)

class AdminModelForm(BootStrapModelForm):
    confirmpassword = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password":forms.PasswordInput
            #如果在密码错误之后，不想他是空的，那就：会保留原来的值
            # "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
    def clean_confirmpassword(self):
        # print(self.cleaned_data)
        # {'username': 'jkl;', 'password': 'iui', 'confirmpassword': 'ooo'}
        print(self.cleaned_data.get("password"))
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirmpassword"))
        if pwd!=confirm:
            raise ValidationError("密码不一致")
        # print(pwd,confirm)
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

def admin_add(request):
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,"change.html",{"form":form,"title":title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)  # 得到form的所有信息
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html",{"form":form,"title":title})


class AdminResetModelForm(BootStrapModelForm):
    confirmpassword = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )
    class Meta:
        model = models.Admin
        fields = ["password"]
        widgets = {
            "password":forms.PasswordInput
            #如果在密码错误之后，不想他是空的，那就：会保留原来的值
            # "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5pwd = pwd
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5pwd).exists()
        if exists:
           raise ValidationError("密码和之前的一样，不行")
        return md5(pwd)
    def clean_confirmpassword(self):
        # print(self.cleaned_data)
        # {'username': 'jkl;', 'password': 'iui', 'confirmpassword': 'ooo'}
        # print(self.cleaned_data.get("password"))
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirmpassword"))
        if pwd!=confirm:
            raise ValidationError("密码不一致")
        # print(pwd,confirm)
        return confirm

def admin_edit(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")
    title = "编辑管理员"
    if request.method == "GET":
        # form = AdminModelForm()
        form = AdminEditModelForm(instance=row_object)
        return render(request,"change.html",{"form":form,"title":title})

    form  = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form":form})



def admin_reset(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")
    title = "重置密码{}".format(row_object.username)
    if request.method =="GET":
        form = AdminResetModelForm()
        return render(request,"change.html",{"form":form,"title":title})
    form = AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(request, "change.html", {"form":form,"title":title})
