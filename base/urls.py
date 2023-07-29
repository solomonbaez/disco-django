from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # primary key routing
    path("room/<str:pk>/", views.room, name="room"),
]
