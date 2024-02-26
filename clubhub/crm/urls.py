from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import ClubDetailView, ClubListView


app_name = 'crm'
urlpatterns = [

    path('', views.HomePageView.as_view(), name="index"),
    path('club/join/<int:pk>',views.joinClub, name='club_join'),
    path('register', views.RegisterFormView.as_view(), name="register"),

    path('login/', views.LoginView.as_view(), name="login"),
    
    path('approval-pending', views.PendingRegisterView.as_view(),name='pending'),

    path('dashboard', views.DashBoardView.as_view(), name="dashboard"),

    path('user-logout', views.user_logout, name="logout"),
   
    path('club/list/', ClubListView.as_view(), name='club_list'),

    path('admin-approve/<int:pk>/<str:approved>', views.ApproveUserView.as_view(), name='approve'),
    path('coord-approve/<int:pk>/<str:approved>', views.ApproveClubUserView.as_view(), name='approve_member'),
    path('club/create', views.ClubCreateView.as_view(), name="create_club"),
    #TODO dont allow access if not logged in
    path('club/coord/<int:pk>', views.ClubCoordinatorCreateView.as_view(), name = 'coord'),
    path('club/<int:pk>',views.ClubDetailView.as_view(),name='club_detail'),
    

]




