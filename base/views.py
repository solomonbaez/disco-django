from django.shortcuts import render
from .models import Room, Message


# function based views
def home(request):
    # object model manager
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    message = Message.objects.all()

    context = {"room": room, "message": message}
    return render(request, "base/room.html", context)


def createRoom(request):
    context = {}
    return render(request, "base/room_form.html", context)
