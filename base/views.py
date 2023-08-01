from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
from .forms import CreateRoomForm


def registerView(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # commit == false -> maintain user mutability
            user = form.save(commit=False)
            # clean data
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "An error occured during registration")

    return render(request, "base/login_register.html", {"form": form, "page": page})


def loginView(request):
    page = "login"
    # restrict login to prevent SID overflow
    if request.user.is_authenticated:
        return redirect("home")

    elif request.method == "POST":
        # clean and parse data
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.INFO, "User does not exist!")

        user = authenticate(request, username=username, password=password)
        if user:
            # create a new session
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(request, messages.INFO, "Failed to authenticate")

    return render(request, "base/login_register.html", {"page": page})


def logoutView(request):
    # deletes session token
    logout(request)

    return redirect("home")


# function based views
def home(request):
    if request.GET.get("q"):
        q = request.GET.get("q")
    else:
        q = ""

    # case insensitive filtering
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
    }

    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    message = Message.objects.all()

    context = {"room": room, "message": message}
    return render(request, "base/room.html", context)


# restrict room creation by SID
@login_required(login_url="login")
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


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = CreateRoomForm(instance=room)

    # prevent non-owners from updating a room
    if request.user != room.host:
        messages.add_message(request, messages.INFO, "You are not the host!")
        return redirect("home")

    elif request.method == "POST":
        # validate form data
        form = CreateRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

        context = {"form": form}

        return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # prevent non-owners from deleting a room
    if request.user != room.host:
        messages.add_message(request, messages.INFO, "You are not the host!")
        return redirect("home")

    elif request.method == "POST":
        # validate form data
        form = CreateRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

        context = {"form": form}

        return render(request, "base/room_form.html", context)
