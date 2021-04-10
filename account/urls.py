from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("creator/", views.register_creator, name="register_creator"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/dashboard/<action>', views.dashboard, name='dashboard'),


]
