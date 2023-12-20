from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0排除不需要验证的url
        # request.path_info  获取当前用户请求的url
        if request.path_info == "/login/":
            return
        # 1\ 读取当前访问的用户的session信息，如果能读到，说明已经登录过，继续向后走就可以了
        info = request.session.get("info")
        if not info:
            return redirect("/login/")
        return
    # def process_response(self, request, response):
    #     print("M1出去了")
    #     return response

