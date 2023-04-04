"""salary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin, auth
from django.urls import path, include
from main import views
from main import get_salary

salary = [
    path('', views.salary),
    path('edit/<int:id>/', views.salary_edit),
    path('edit/<int:id>/add/bonuse', views.add_bonuse),
    path('edit/<int:id>/add/sanction', views.add_sanction),
    path('delete/<int:id>/', views.salary_delete),
]

urlpatterns = [
    path('', views.index),
    path('salary/', include(salary)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register_request ),
]
