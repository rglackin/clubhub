from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import ClubDetailView, ClubListView


app_name = 'crm'
urlpatterns = [

    path('', views.HomePageView.as_view(), name="index"),

    path('register', views.RegisterFormView.as_view(), name="register"),


    path('login/', views.LoginView.as_view(), name="login"),
    

    path('approval-pending', views.PendingRegisterView.as_view(),name='pending'),

    path('dashboard', views.DashBoardView.as_view(), name="dashboard"),

    path('user-logout', views.user_logout, name="logout"),

    path('admin-approve', views.ApproveUserView.as_view(), name='approve'),

    path('club_detail/<int:pk>/', ClubDetailView.as_view(), name='club_detail'),
    path('club_list/', ClubListView.as_view(), name='club_list'),

]




