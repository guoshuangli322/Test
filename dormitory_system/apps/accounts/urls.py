from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 登录/登出
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 修改密码
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/password_done/'
    ), name='change_password'),
    path('password_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_done.html'
    ), name='password_done'),

    # 用户管理（超级管理员）
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('user/add/', views.UserCreateView.as_view(), name='user_add'),
    path('user/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]
