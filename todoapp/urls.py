"""
URL configuration for todoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from todolist.views import TaskDelete, TaskList, TaskDetail, TaskCreate, TaskUpdate, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('swagger/', TemplateView.as_view(
        template_name='index.html',
        extra_context={'schema_url': 'swagger/openapi_spec.json'}
    ), name='swagger-ui'),

    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    
    path('', TaskList.as_view(), name='tasks'),
    path('task/<uuid:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<uuid:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<uuid:pk>', TaskDelete.as_view(), name='task-delete'),
]
