from django.shortcuts import render, redirect
from .models import Room, Message, Topic
from .forms import CreateRoomForm


# function based views
def home(request):
    if request.GET.get("q"):
        q = request.GET.get("q")
    else:
        q = ""

    # case insensitive filtering
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    context = {
        "rooms": rooms,
        "topics": topics,
    }

    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    message = Message.objects.all()

    context = {"room": room, "message": message}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = CreateRoomForm()
    if request.method == "POST":
        # parse form data
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = CreateRoomForm(instance=room)
    if request.method == "POST":
        # validate form data
        form = CreateRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}

    return render(request, "base/room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/room_delete.html", {"obj": room})
