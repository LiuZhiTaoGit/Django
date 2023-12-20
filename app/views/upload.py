from app import models
from django import forms

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

def upload_list(request):
    if request.method =="GET":
        return render(request, "upload_list.html")
    # print(request.POST)  # 请求体的数据
    # print(request.FILES) # 请求体的文件
    # 之前是：'username': ['aaa'], 'avatar': ['2.docx']}>
    # 加上：  <form method="post" enctype="multipart/form-data">后：
    # < form
    # method = "post"
    # enctype = "multipart/form-data" >

    file_object = request.FILES.get("avatar")   # N
    print(file_object.name)  # 联邦学习客户信用评价仿真软件.pdf  文件名


    return HttpResponse("...")

