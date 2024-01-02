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
from rest_framework.routers import DefaultRouter
from performances import views

router = DefaultRouter()
router.register(r'instructors', views.InstructorViewSet, basename='instructors')
router.register(r'students', views.StudentViewSet, basename='students')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),  # include the router.urls under an 'api/' path
    path('api/performance/', views.performance_list, name='performances-get-list'),
    path('api/category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('api/performance-update/<int:pk>/', views.PerformanceUpdateView.as_view(), name='performance-update'),
    path('api/performance-accessory/add/', views.PerformanceAccessoryCreateView.as_view(), name='performance-accessory-add'),
    path('api/performance-accessory-update/<int:perf_pk>/<int:acc_pk>/', views.PerformanceAccessoryUpdateView.as_view(), name='performance-accessory-update'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.home, name="home"),
    path("performance/add/", views.performance_add.as_view(), name="performance_add"),
    path("performance/<int:pk>/", views.performance_detail, name="performance_detail"),
    path("performance/<int:pk>/edit", views.performance_edit, name="performance_edit"),
    path("performance/<int:pk>/instructors/", views.performance_instructors, name="performance_instructors"),
    path("performance/<int:pk>/instructors/add/", views.instructor_add.as_view(), name="performance_instructors_add"),
    path("performance/<int:perf_pk>/instructors/<int:instr_pk>/edit/", views.instructor_edit, name="instructor_edit"),
    path("performance/<int:pk>/students/", views.performance_students, name="performance_students"),
    path("performance/<int:pk>/students/add/", views.student_add.as_view(), name="performance_students_add"),
    path("performance/<int:perf_pk>/students/<int:stud_pk>/edit/", views.student_edit, name="student_edit"),
    path("performance/<int:pk>/accessories/", views.performance_accessories, name="performance_accessories"),
    path("select-fair/", views.select_fair, name="select_fair"),
    path("select-fair/<int:pk>/", views.select_fair, name="set_fair"),
    path("edit-fair/<int:pk>/", views.edit_fair, name="edit_fair"),

]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
