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
   
    path('club/list/', ClubListView.as_view(), name='club_list'),

    path('user/profile/<int:pk>',views.UserDetailView.as_view(),name='user_profile'),
    path('user/profile/update/<int:pk>',views.UserUpdateView.as_view(),name='user_update'),
    path('club/join/<int:pk>',views.joinClub, name='club_join'),
    path('admin-approve/<int:pk>/<str:approved>', views.ApproveUserView.as_view(), name='approve'),
    path('coord-approve/<int:pk>/<str:approved>', views.ApproveClubUserView.as_view(), name='approve_member'),
    path('club/create', views.ClubCreateView.as_view(), name="create_club"),
    #TODO dont allow access if not logged in
    path('club/coord/<int:pk>', views.ClubCoordinatorCreateView.as_view(), name = 'coord'),
    path('club/<int:pk>',views.ClubDetailView.as_view(),name='club_detail'),
    
    path('club/event/create/<int:pk>', views.EventCreateView.as_view(),name='create_event'),
    path('club/event/list/<int:pk>', views.EventListView.as_view(), name='event_list'),
    path('club/event/detail/<int:pk>',views.EventDetailView.as_view(), name='event_detail'),
    path('club/event/join/<int:pk>',views.event_join,name='event_join'),
    path('club/event/manage/<int:pk>',views.EventManageView.as_view(),name='event_manage'),
    path('club/event/approve/<int:pk>/<str:approved>', views.event_approve, name='approve_event'),
]




