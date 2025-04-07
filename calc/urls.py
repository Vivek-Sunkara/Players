from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),  # <- FIXED HERE
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('creator/', views.creator_form, name='creator_form'),
    path('addplayer/<str:session_id>/', views.add_player, name='add_player'),
    path('generateteam/<str:session_id>/', views.generate_team, name='generate_team'),
]
