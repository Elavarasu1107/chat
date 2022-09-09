from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLogin.as_view(), name='login'),
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]
