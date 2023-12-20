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
def depart_list(request):
    """部门列表"""
    # 检查用户是否已经登录，如果登录了才可以展示，如果没登录，跳回登录页面
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    queryset = models.Department.objects.all()
    page_object = Pagination(request, queryset,page_size=2)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    # return render(request, 'pretty_list.html', context)

    return render(request, "depart_list.html", context)

def depart_add(request):
    if request.method == "GET":
        return render(request, "depart_add.html")
    part_name = request.POST.get("part_name")
    models.Department.objects.create(title = part_name)
    return redirect("/depart/list")

def depart_delete(request):
    # ids = request.POST.get("id")
    nid = request.GET.get("nid")
    # models.Department.objects.filter(id=ids)
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list")
def depart_edit(request,nid):
    if request.method =="GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html",{"title":row_object.title})
    # edit_name = request.POST.get("edit_name")
    # models.Department.objects.filter(title = )
    par_name = request.POST.get("part_name")
    models.Department.objects.filter(id=nid).update(title=par_name)
    return redirect('/depart/list')