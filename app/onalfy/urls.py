"""
URL configuration for onalfy project.

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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from performances import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/performance/', views.performance_list, name='performances-get-list'),
    path('api/category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('api/performance-update/<int:pk>/', views.PerformanceUpdateView.as_view(), name='performance-update'),
    path('api/instructors/', views.instructor_list, name='instructors-get-list'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.home, name="home"),
    path("performance/<int:pk>/", views.performance_detail, name="performance_detail"),
    path("performance/<int:pk>/instructors/", views.performance_instructors, name="performance_instructors"),
    path("performance/<int:pk>/instructors/add/", views.instructor_add.as_view(), name="performance_instructors_add"),
    path("performance/add/", views.performance_add.as_view(), name="performance_add"),
    path("select-fair/", views.select_fair, name="select_fair"),
    path("select-fair/<int:pk>/", views.select_fair, name="set_fair"),
    path("edit-fair/<int:pk>/", views.edit_fair, name="edit_fair"),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
