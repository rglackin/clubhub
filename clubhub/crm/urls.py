from django.urls import path

from . import views
app_name = 'crm'
urlpatterns = [

    path('', views.HomePageView.as_view(), name="index"),

    path('register', views.RegisterFormView.as_view(), name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
    
]











