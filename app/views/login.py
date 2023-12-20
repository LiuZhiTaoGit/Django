from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from app import models
from app.utils.encrypt import md5



class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required=True#这个必须填写
        # widget=forms.Textarea(attrs={"class":"form-control"}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        required=True  # 这个必须填写
    )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

#这两个的效果是一样的
# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Admin
#         fields = ["username","password"]



def login(request):
    if request.method =="GET":
        form = LoginForm()
        return render(request, "login.html",{"form":form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # {'username': '123', 'password': '456'}
        #去数据库校验  如果没有得到，返回为空
        #下面的这个会更加简介
        # admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'], password = form.cleaned_data['password']).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:# 用户名和密码错误
            form.add_error("password","用户名或者密码错误！！！")
            return render(request, "login.html", {"form": form})


        #用户名和密码正确
        request.session["info"] = {"id":admin_object.id, "name":admin_object.username}
        # return HttpResponse("提交成功")
        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})
