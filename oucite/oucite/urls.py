"""
URL configuration for oucite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", view=include("blog.urls"))
]

# 浏览器访问/article/3/，发送 HTTP GET 请求。通过项目级urls.py里指定的模式进行URL匹配之后转给blog/url.py （这里用了 include），匹配到"article/<int:pk>/"的路径(pk为3)，调用article_detail视图函数。
# 视图用 ORM 查询 pk=3 的 Article 对象，若未查到，抛出 Http404，查到则浏览量+1并调用render。
# render 把文章对象给模板渲染成 HTML，最终包装成 HttpResponse 返回浏览器。
