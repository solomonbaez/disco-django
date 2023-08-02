from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
from .forms import CreateRoomForm, UserForm


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

    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "recent_messages": recent_messages,
    }

    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    # query children of current room
    room_messages = room.message_set.all().order_by("created")

    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        # redirect to parse POST -> prevent GET conflict
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "topics": topics,
        "room_messages": room_messages,
        "recent_messages": room_messages,
    }
    return render(request, "base/profile.html", context)


# restrict room creation by SID
@login_required(login_url="login")
def createRoom(request):
    form = CreateRoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        # parse form data
        topic_name = request.POST.get("topic")
        # parse topics -> create new if needed
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

        # form = CreateRoomForm(request.POST, topic=topic)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = CreateRoomForm(instance=room)

    # prevent non-owners from updating a room
    if request.user != room.host:
        messages.add_message(request, messages.INFO, "You are not the host!")
        return redirect("home")

    elif request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.topic = topic
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")

        room.save()
        return redirect("home")

    context = {
        "form": form,
        "topics": topics,
        "room": room,
        "update_or_delete": "update",
    }

    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.add_message(request, messages.INFO, "You are not the host!")

    elif request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.add_message(request, messages.INFO, "You are not the host!")

    elif request.method == "POST":
        message.delete()
        return redirect("room", pk=message.room.id)

    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def updateUser(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=pk)
    return render(request, "base/update-user.html", {"form": form})
