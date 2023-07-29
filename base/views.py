from django.shortcuts import render

rooms = [
    {"id":1, "name":"Django Practice!"},
    {"id":2, "name":"Frontend Practice!"},
    {"id":3, "name":"Backend Practice!"},
]

# function based views
def home(request):
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request):
    return render(request, "base/room.html")
