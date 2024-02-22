from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'crm'
urlpatterns = [

    path('', views.HomePageView.as_view(), name="index"),

    path('register', views.RegisterFormView.as_view(), name="register"),


    path('login/', views.LoginView.as_view(), name="login"),
    
   # path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.HomePageView.as_view(), name='index'),
]




