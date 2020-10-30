"""为应用程序 users 定义 URL 模式"""

from django.urls import path, include

from . import views


app_name = 'users'

urlpatterns = [
    # 包含默认的身份验证URL
    path('', include('django.contrib.auth.urls')),
    # 注册页面
    path('register/', views.register, name='register')
]