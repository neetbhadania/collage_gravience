from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('viewdata/', views.viewdata, name='viewdata'),
    path('student-grievance/', views.grievance_form, name='student_grievance'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('register/', views.register, name='register'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-grievances/', views.admin_grievances, name='admin_grievances'),
    path('admin-grievances/delete/<int:id>/', views.delete_grievance, name='delete_grievance'),
    path('admin-grievances/edit/<int:id>/', views.edit_grievance, name='edit_grievance'),
]
