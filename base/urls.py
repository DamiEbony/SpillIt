from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics-page/', views.topicsPage, name='topics-page'),
    path('latest-page/', views.latestPage, name='latest-page'),
    
    
    
    path('', views.home, name='home'),
    
    path('room/<str:pk>/', views.room, name='room'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
     path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
     path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
     path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    
    
    
    
    

]

