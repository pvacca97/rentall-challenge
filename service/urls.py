"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns

from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', views.TaskList.as_view(), name='tasks'),
    path('task/', views.TaskDetail.as_view(), name='task_generic'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task_detail_pk'),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('category/', views.CategoryDetail.as_view(), name='category_detail'),
    path('category/<str:pk>/', views.CategoryDetail.as_view(), name='category_detail_pk'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
