"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import depart, prety, user, admin, account, task, order, chart, upload
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path("/",views.login)
    path("depart/list/",depart.depart_list),
    path("depart/add/",depart.depart_add),
    path("depart/delete/",depart.depart_delete),
    path("depart/<int:nid>/edit/",depart.depart_edit),

    path("user/list/",user.user_list),
    path("user/add/",user.user_add),
    path("user/model/form/add/",user.user_model_form_add),
    path("user/<int:nid>/edit/",user.user_edit),
    path("user/<int:nid>/delete/",user.delete_user),

    path("pretty/list/",prety.pretty_list),
    path("pretty/add/",prety.pretty_add),
    path("pretty/<int:nid>/delete/",prety.pretty_delete),
    path("pretty/<int:nid>/edit/",prety.pretty_edit),

    path("admin/list/",admin.admin_list),
    path("admin/add/",admin.admin_add),
    path("admin/<int:nid>/edit/",admin.admin_edit),
    path("admin/<int:nid>/reset/",admin.admin_reset),

    path("login/",account.login),
    path("logout/",account.logout),

    path("task/list/",task.task_list),
    path("task/ajax/",task.task_ajax),
    path("task/add/",task.task_add),


    #订单
    path("order/list/",order.order_list),
    path("order/add/",order.order_add),
    path("order/delete/",order.order_delete),
    path("order/edit/",order.order_edit),
    path("order/detail/",order.order_detail),

    path("chart/list/",chart.chart_list),
    path("chart/bar/",chart.chart_bar),
    path("chart/pie/",chart.chart_pie),
    path("chart/High/",chart.highchart),

#     文件上传
    path("upload/list/",upload.upload_list),



]
