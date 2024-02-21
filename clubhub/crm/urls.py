from django.urls import path

from . import views
app_name = 'crm'
urlpatterns = [

    path('', views.HomePageView.as_view(), name="index"),

    path('register', views.RegisterFormView.as_view(), name="register"),

    path('login', views.LoginView.as_view(), name="login"),
    
    path('logout', views.LogoutView.as_view(),name='logout'),
   # path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
    
]











