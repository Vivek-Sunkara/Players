from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    profile_view, player_detail_view, create_team, add_players,
    player_form_view, create_team_view, optimize_team_view, register
)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('player/<int:player_id>/', player_detail_view, name='player_detail'),
    path('create-team/', create_team, name='create_team'),
    path('add-players/<int:team_id>/', add_players, name='add_players'),
    path('player-form/<uuid:unique_link>/', player_form_view, name='player_form'),
    path('optimize-team/<int:creator_id>/', optimize_team_view, name='optimize_team'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
