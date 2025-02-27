"""
URL configuration for onaylf project.

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
from submissions import views
from users.views import SignUpView, user_account_detail, user_account_edit, user_edit, organization_list, organization_add, organization_edit, organization_delete, confirm_user, delete_user, user_add, admin_password_reset, admin_password_reset_done

handler500 = 'submissions.views.custom_500_view'

router = DefaultRouter()
router.register(r'instructors', views.InstructorViewSet, basename='instructors')
router.register(r'students', views.StudentViewSet, basename='students')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),  # include the router.urls under an 'api/' path
    path('api/submission/', views.submission_list, name='submissions-get-list'),
    path('api/poster/', views.poster_list, name='posters-get-list'),
    # path('api/submission-poster/', views.submission_poster_list, name='submissions-posters-get-list'),
    path('api/submission/<int:perf_pk>/', views.submission_get, name='submission-get'),
    path('api/category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('api/submission-update/<int:pk>/', views.SubmissionUpdateView.as_view(), name='submission-update'),
    path('api/submission-accessory/add/', views.SubmissionAccessoryCreateView.as_view(), name='submission-accessory-add'),
    path('api/submission-accessory-update/<int:perf_pk>/<int:acc_pk>/', views.SubmissionAccessoryUpdateView.as_view(), name='submission-accessory-update'),
    path('api/instructor/add/', views.InstructorAddView.as_view(), name='instructor-add'),
    path('api/instructor/update/<int:instr_pk>/', views.InstructorUpdateView.as_view(), name='instructor-update'),
    path('api/student/add/', views.StudentAddView.as_view(), name='student-add'),
    path('api/student/update/<int:stud_pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('api/fair/<int:fair_pk>/download/', views.FairDownloadView.as_view(), name='fair-download'),
    path('api/fair/<int:fair_pk>/download-judge-sheets/', views.JudgeSheetsDownloadView.as_view(), name='fair-download-judge-sheets'),
    path('api/fair/<int:fair_pk>/download-submission-sheets/', views.SubmissionSheetsDownloadView.as_view(), name='fair-download-submission-sheets'),
    path('api/fair/<int:fair_pk>/download-submission-cards/', views.SubmissionCardsDownloadView.as_view(), name='fair-download-submission-cards'),
    path('api/fair/<int:fair_pk>/download-registration-cover-sheets/', views.RegistrationCoverSheetsDownloadView.as_view(), name='fair-download-registration-cover-sheets'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile/', user_account_detail, name='user_account_detail'),
    path('accounts/profile/edit/', user_account_edit, name='user_account_edit'),
    path("", views.home, name="home"),
    path("contact/", views.contact_info, name="contact"),
    path("users/", views.user_list, name="user_list"),
    path("user/<int:user_pk>/", views.user_detail, name="user_detail"),
    path('user/<int:user_id>/edit/', user_edit, name='user_edit'),
    path("user/<int:user_pk>/submission/add/", views.submission_add_admin.as_view(), name="submission_add_admin"),
    path("user/<int:user_pk>/submission/add/<str:category>/", views.submission_add_admin.as_view(), name="submission_add_admin_with_category"),
    path("user/<int:user_pk>/poster/add/", views.poster_add.as_view(), name="poster_add_admin"),
    path("user/<int:user_pk>/poster/add/instructor/add/", views.instructor_add.as_view(), name="poster_add_instructor_add_admin"),
    path("user/<int:user_pk>/poster/add/instructors/<int:instr_pk>/edit/", views.instructor_edit, name="poster_add_instructor_edit_admin"),
    path("user/<int:user_pk>/poster/add/student/add/", views.student_add.as_view(), name="poster_add_student_add_admin"),
    path("user/<int:user_pk>/poster/add/students/<int:stud_pk>/edit/", views.student_edit, name="poster_add_student_edit_admin"),
    path("submission/add/", views.submission_add.as_view(), name="submission_add"),
    path("submission/add/<str:category>/", views.submission_add.as_view(), name="submission_add_with_category"),
    path("submission/<int:perf_pk>/", views.submission_detail, name="submission_detail"),
    path("submission/<int:perf_pk>/edit/", views.submission_edit, name="submission_edit"),
    path("submission/<int:perf_pk>/instructors/", views.submission_instructors, name="submission_instructors"),
    path("submission/<int:perf_pk>/instructors/add/", views.instructor_add.as_view(), name="submission_instructors_add"),
    path("submission/<int:perf_pk>/instructors/<int:instr_pk>/edit/", views.instructor_edit, name="instructor_edit"),
    path("submission/<int:perf_pk>/students/", views.submission_students, name="submission_students"),
    path("submission/<int:perf_pk>/students/add/", views.student_add.as_view(), name="submission_students_add"),
    path("submission/<int:perf_pk>/students/<int:stud_pk>/edit/", views.student_edit, name="student_edit"),
    path("submission/<int:perf_pk>/accessories/", views.submission_accessories, name="submission_accessories"),
    path("submission/<int:perf_pk>/review/", views.submission_review, name="submission_review"),
    path("students/", views.student_list, name="student_list"),
    path("poster/add/", views.poster_add.as_view(), name="poster_add"),
    path("poster/<int:post_pk>/", views.poster_detail, name="poster_detail"),
    path("poster/<int:post_pk>/edit/", views.poster_edit, name="poster_edit"),
    path("poster/add/instructor/add/", views.instructor_add.as_view(), name="poster_add_instructor_add"),
    path("poster/add/instructors/<int:instr_pk>/edit/", views.instructor_edit, name="poster_add_instructor_edit"),
    path("poster/add/student/add/", views.student_add.as_view(), name="poster_add_student_add"),
    path("poster/add/students/<int:stud_pk>/edit/", views.student_edit, name="poster_add_student_edit"),
    path("select-fair/", views.select_fair, name="select_fair"),
    path("select-fair/<int:pk>/", views.select_fair, name="set_fair"),
    path("edit-fair/<int:pk>/", views.edit_fair, name="edit_fair"),
    path("fair-info/", views.fair_detail, name="fair_detail"),
    path("migrate/", views.migrate_data, name="migrate_data"),
    # path("pen/", views.query_inveniordm, name="pen")
    path('programs/', organization_list, name='organization_list'),
    path('programs/add/', organization_add, name='organization_add'),
    path('programs/<int:pk>/edit/', organization_edit, name='organization_edit'),
    path('programs/<int:pk>/delete/', organization_delete, name='organization_delete'),
    path('fairs/', views.fair_list, name='fair_list'),
    path('api/fairs/<int:pk>/', views.get_fair, name='fair_get'),
    path('api/fairs/<int:pk>/edit/', views.edit_fair, name='fair_edit'),
    
    # URLs for related items
    path('api/fairs/<int:fair_id>/languoids/', views.handle_languoid, name='fair_languoid_add'),
    path('api/fairs/<int:fair_id>/languoids/<int:item_id>/', views.handle_languoid, name='fair_languoid_edit'),
    path('api/fairs/<int:fair_id>/languoids/<int:item_id>/check_delete/', views.check_delete_item, {'type': 'languoids'}, name='fair_languoid_check_delete'),
    
    path('api/fairs/<int:fair_id>/tribes/', views.handle_tribe, name='fair_tribe_add'),
    path('api/fairs/<int:fair_id>/tribes/<int:item_id>/', views.handle_tribe, name='fair_tribe_edit'),
    path('api/fairs/<int:fair_id>/tribes/<int:item_id>/check_delete/', views.check_delete_item, {'type': 'tribes'}, name='fair_tribe_check_delete'),
    
    path('api/fairs/<int:fair_id>/categories/', views.handle_category, name='fair_category_add'),
    path('api/fairs/<int:fair_id>/categories/<int:item_id>/', views.handle_category, name='fair_category_edit'),
    path('api/fairs/<int:fair_id>/categories/<int:item_id>/check_delete/', views.check_delete_item, {'type': 'categories'}, name='fair_category_check_delete'),
    
    path('api/fairs/<int:fair_id>/accessories/', views.handle_accessory, name='fair_accessory_add'),
    path('api/fairs/<int:fair_id>/accessories/<int:item_id>/', views.handle_accessory, name='fair_accessory_edit'),
    path('api/fairs/<int:fair_id>/accessories/<int:item_id>/check_delete/', views.check_delete_item, {'type': 'accessories'}, name='fair_accessory_check_delete'),
    path('api/fairs/<int:fair_id>/categories/<int:category_id>/check_delete/', views.check_category_delete, name='check_category_delete'),
    path('api/fairs/<int:fair_id>/languoids/<int:languoid_id>/check_delete/', views.check_languoid_delete, name='check_languoid_delete'),
    path('api/fairs/<int:fair_id>/tribes/<int:tribe_id>/check_delete/', views.check_tribe_delete, name='check_tribe_delete'),
    path('api/fairs/<int:fair_id>/accessories/<int:accessory_id>/check_delete/', views.check_accessory_delete, name='check_accessory_delete'),
    path('api/fair/<int:fair_pk>/', views.get_fair_data, name='get_fair_data'),
    path('fairs/add/', views.add_fair, name='add_fair'),
    path('api/set_current_fair/', views.set_current_fair, name='set_current_fair'),
    path('api/confirm-user/<int:user_id>/', confirm_user, name='confirm_user'),
    path('api/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('api/submission/<int:submission_id>/delete/', views.submission_delete, name='submission_delete'),
    path('user/add/', user_add, name='user_add'),
    path('api/students/<int:student_id>/check_delete/', views.check_student_delete, name='check_student_delete'),
    path('api/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('accounts/admin_password_reset/<int:user_id>/', admin_password_reset, name='admin_password_reset'),
    path('accounts/admin_password_reset/<int:user_id>/done/', admin_password_reset_done, name='admin_password_reset_done'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
