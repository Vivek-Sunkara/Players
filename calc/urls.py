from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_page, name='base'),  # ✅ Make this the homepage
    path('home/', views.home_view, name='home'),  # 🔁 Moved to a separate route
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('creator/', views.creator_form, name='creator_form'),
    path('addplayer/<str:session_id>/', views.add_player, name='add_player'),
    path('generateteam/<str:session_id>/', views.generate_team, name='generate_team'),
]
