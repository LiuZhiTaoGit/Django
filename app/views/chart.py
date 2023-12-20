from app import models
from django import forms

from django.shortcuts import render, redirect
from django.http import JsonResponse

def chart_list(request):
    """数据统计页面"""
    return render(request, 'chart_list.html')
def chart_pie(request):

    series_list = [
        {"value": 1048, "name": 'IT部门'},
        {"value": 735, "name": '运行部门'},
        {"value": 580, "name": '新媒体部门'},
    ]
    result = {
        "status":True,
        "data":series_list
    }
    return JsonResponse(result)

def chart_bar(request):
    """构造柱状图数据"""
    # s数据库中可以获取
    legend = ['张三','李四']
    series_list = [
        {
            "name": '张三',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '李四',
            "type": 'bar',
            "data": [50, 230, 336, 140, 150, 230]
        }
    ]
    xAxis_list = ['1月', '2月', '3月', '4月', '5月', '6月']
    result = {
        "status":True,
        "data":{
            'legend':legend,
            "series":series_list,
            "xAxis":xAxis_list
        }
    }
    return JsonResponse(result)


def highchart(request):
    return render(request,'chart_high.html')