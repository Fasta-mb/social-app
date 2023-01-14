from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', views.ChangePassword.as_view(), name='change-password'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='auths/password_change_done.html'), name='password-change-done'),
    
]
