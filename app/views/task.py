from django.shortcuts import render, HttpResponse
import json
from .. import models
from django.views.decorators.csrf import csrf_exempt#免除csrf的验证
from app import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from ..utils.pagination import Pagination
from ..utils.bootstrap import BootStrapModelForm
from ..utils.pagination import Pagination

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            "detail":forms.TextInput
        }

def task_list(request):
    """任务列表"""
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)

    form = TaskModelForm()
    context = {
        "form" : form,
        "queryset":page_object.page_queryset,
        "page_string":page_object.html()
    }

    return render(request, "task_list.html",context)





@csrf_exempt
def task_add(request):
    data = request.POST
    # data_dict = {"status":True, "data":data}
    # json_str = json.dumps(data_dict)
    # print(json_str)
    # {"status": true, "data": {"level": "3", "title": "\u89e3\u5f00\u4e86", "detail": "\u5c3d\u5feb", "user": "7"}}

    # 1、 对用户的数据进行校验,使用modelform进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status":True}
        #这里就不用跳转了，也需要返回一个json
        return HttpResponse(json.dumps(data_dict))
    print(form.errors.as_json())
    from django.forms.utils import ErrorDict
    data_dict = {"status":False, "error":form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))#让他显示中文的错误

@csrf_exempt
def task_ajax(request):
    print("get:",request.GET)
    print("post:",request.POST)

    data_dict = {"status":True, "data":request.POST}
    json_str = json.dumps(data_dict)
    return HttpResponse(json_str)