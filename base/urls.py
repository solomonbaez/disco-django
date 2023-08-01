from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerView, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("", views.home, name="home"),
    # primary key routing
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),
    path(
        "delete-message/<str:mk>/<str:pk>/", views.deleteMessage, name="delete-message"
    ),
]
