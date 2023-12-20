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



def pretty_list(request):
    """靓号列表"""
    # 检查用户是否已经登录，如果登录了才可以展示，如果没登录，跳回登录页面
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PretyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset,page_size=10)
    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'pretty_list.html', context)


    # for i in range(200):
    #     models.PretyNum.objects.create(mobile="1881524587",price=60,level=1,status=1)

    # q1 = models.PretyNum.objects.filter(mobile="15265585505")
    # print(q1)
    # #多个条件，可以放到字典中
    # data_dict = {
    #     "mobile":"15265585505"
    # }
    # q2 = models.PretyNum.objects.filter(**data_dict)
    # print(q2)




    #
    #
    #
    # data_dict = {}
    # search_data = request.GET.get('q',"")
    # if search_data:
    #     data_dict["mobile__contains"] = search_data
    # # from .utils import pagination.pagination.Pagination
    # # from utils import pagination
    # #分页
    #
    # #
    # # from app.pagination import Pagination
    # # # from utils.pagination import Pagination
    # # Pagination(request)
    # # Pagination(request)
    # # Pagination(request)
    #
    #
    #
    # page = int(request.GET.get("page",1))
    # page_size = 10
    # start = (page-1) * page_size
    # end = page * page_size
    #
    # # 控制后台的页码数量
    # page_str_list = []
    # total_count = models.PretyNum.objects.filter(**data_dict).order_by("-level").count()
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1
    # # 计算出当前页的前5后5
    # plus = 5
    # start_page = page - plus
    # end_page = page + plus + 1
    # # print(page,start_page,end_page)
    #
    # #考虑极值的情况
    # if start_page<1:
    #     start_page = 1
    # if end_page >= total_page_count:
    #     end_page = total_page_count
    # if page<plus:
    #     start_page = 1
    #     end_page = 2 *plus +1
    # if page+plus>total_page_count:
    #     start_page = total_page_count-2*plus
    # #首尾页
    # head = '<li><a href="?page={}">首页</a></li>'.format(1)
    # page_str_list.append(head)
    # #上一页下一页
    # if(page!=1):
    #     prev = ' <li ><a href="?page={}">上一页</a></li>'.format(page-1)
    #     page_str_list.append(prev)
    #
    # for i in range(start_page,end_page+1): # range是前取后不取
    #     if page == i:
    #         ele = ' <li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = ' <li><a href="?page={}">{}</a></li>'.format(i,i)
    #     page_str_list.append(ele)
    # #下一页
    # if (page!=total_page_count):
    #     prev = ' <li ><a href="?page={}">下一页</a></li>'.format(page + 1)
    #     page_str_list.append(prev)
    #
    # # 首尾页
    # tail = '<li ><a href="?page={}">首页</a></li>'.format(total_page_count)
    # page_str_list.append(tail)
    #
    # page_str = mark_safe("".join(page_str_list))
    #
    # # res = models.PretyNum.objects.filter(**data_dict)
    # # print(res)
    #
    # # 按照level降序排序  以下 是搜索所有的
    # # queryset = models.PretyNum.objects.all().order_by("-level")
    #
    # queryset = models.PretyNum.objects.filter(**data_dict).order_by("-level")[start:end]
    # return render(request, "pretty_list.html", {"queryset":queryset,"search_data":search_data, "page_str":page_str})

class PrettyModelForm(BootStrapModelForm):
    #验证方式1：
    mobile = forms.CharField(
        validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误")],
        label="手机号"
    )
    class Meta:
        model = models.PretyNum
        # fields = ["id", "mobile", "price", "level","status"]
        fields = "__all__"
        # exclude = ['level']
    #继承的BootStarp
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class":"form-control", "placeholder":field.label}

    # 验证方式2：
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #     #验证不通过：
    #     if len(txt_mobile)!=11:
    #         raise ValidationError("格式错误")
    #     return txt_mobile

    # 新建手机号时，不能有存在的，这个验证方式只能用钩子实现
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PretyNum.objects.filter(mobile=txt_mobile).exists()
        #验证不通过：
        if exists:
            raise ValidationError("手机号已经存在了")
        return txt_mobile
class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True)
    class Meta:
        model = models.PretyNum
        # fields = ["id", "mobile", "price", "level","status"]
        # fields = "__all__"
        exclude = []
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class":"form-control", "placeholder":field.label}

    # 新建手机号时，不能有存在的，这个验证方式只能用钩子实现
    #这个是编辑的时候存在，因为编辑的时候，该数据肯定已经在数据库了，因此要进行修改
    #狗子可以对数据集进行处理，而上面的是不行的
    def clean_mobile(self):
        #得到id   primarykey
        # self.instance.pk   使用exclude排除
        # exists = models.PretyNum.objects.filter(mobile=txt_mobile).exists().exclude(id=self.instance.pk)

        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PretyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        # 验证不通过：
        if exists:
            raise ValidationError("手机号已经存在了")
        return txt_mobile

def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form":form})
    #利用modelform得到request。post的data
    form = PrettyModelForm(data=request.POST)
    #验证数据集，如果没问题，就保存，否则就重新渲染错误的数据
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form":form})

def pretty_delete(request,nid):
    models.PretyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")

def pretty_edit(request, nid):
    row_object = models.PretyNum.objects.filter(id=nid).first()
    if request.method =="GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html",{"form":form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html",{"form":form})