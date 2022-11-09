from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLogin.as_view(), name='login'),
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('index/', views.get_group, name='get_group'),
    path('create/', views.post_group, name='create_group'),
    path('update/<int:id>/', views.put_group, name='update_group'),
    path('delete/<int:id>/', views.delete_group, name='delete_group'),
    path('add_members/<int:group_id>/', views.add_members, name='add_members'),
    path('add_members/<int:group_id>/<int:user_id>/', views.add_members, name='add_members'),
    path('get_members/<int:id>/', views.get_members, name='get_members'),
    path('delete_members/<int:group_id>/<int:user_id>/', views.delete_members, name='delete_members'),
]
