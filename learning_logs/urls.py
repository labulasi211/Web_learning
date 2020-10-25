"""定义 laerning_logs 的 URL 模式"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 显示所有主题
    path('topics/', views.topics, name='topics'),
    # 特定主题的详情页
    path('topics/<int:topic_id>/', views.topic, name='topic')
]