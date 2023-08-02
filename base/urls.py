from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerView, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("", views.home, name="home"),
    # primary key routing
    path("room/<str:pk>/", views.room, name="room"),
    path("user-profile/<str:pk>", views.userProfile, name="user-profile"),
    path("update-user/<str:pk>", views.updateUser, name="update-user"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
    path("mobile-topics", views.mobileTopics, name="mobile-topics"),
    path("mobile-activity", views.mobileActivity, name="mobile-activity"),
]
