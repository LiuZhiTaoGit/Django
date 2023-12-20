from django.shortcuts import render, redirect
from ..utils.bootstrap import BootStrapModelForm
from app import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime
from ..utils.pagination import Pagination

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid","admin"]
@csrf_exempt
def order_add(request):
    """创建订单(ajax请求)"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # meiyou  oid
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        # 管理员也不添加了，使用当前登录的用户
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status":True} )
    return JsonResponse({"status":False,"error":form.errors} )


def order_detail(request):
    """根据id获取订单信息"""
    # 方式1
    """uid = request.GET.get("uid")
#     拿到当前行的对象
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status:":False,'error':"数据不存在"})
    # 已经得到了对象，需要获取值
    # row_object.title
    result = {
        "status":True,
        "data":{
            "title":row_object.title,
            "price":row_object.price,
            "status":row_object.status,
        }
    }
    return JsonResponse({"status":True,'data':result})"""


    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("id","title","price","status").first()
    if not row_dict:
        return JsonResponse({"status:": False, 'error': "数据不存在"})
    result = {
        "status": True,
        "data": row_dict
    }
    # row_object.title
    return JsonResponse(result)

    # form = OrderModelForm(instance=row_object)

def order_delete(request):
    uid = request.GET.get("uid")
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status":True})
@csrf_exempt
def order_edit(request):
    """编辑页面"""
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not  row_object:
        return JsonResponse({"status":False, 'tips':"数据不存在"})
    form = OrderModelForm(data= request.POST, instance=row_object)


    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False ,'error':form.errors})


def order_list(request):

    queryset = models.Order.objects.all().order_by('-id')
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    # return render(request, 'pretty_list.html', context)

    # form = OrderModelForm()
    return render(request, "order_list.html",context)