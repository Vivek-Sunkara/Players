from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('player/<int:player_id>/', views.player_detail_view, name='player_detail'),
    path('create-team/', views.create_team, name='create_team'),
    path('add-players/<int:team_id>/', views.add_players, name='add_players'),
    path('player-form/<uuid:unique_link>/', views.player_form_view, name='player_form'),
    path('optimize-team/<int:creator_id>/', views.optimize_team_view, name='optimize_team_with_id'),
    path('optimize-team/', views.optimize_team_view, name='optimize_team'),
    path('accounts/', include('django.contrib.auth.urls')),
]
