from django.forms import ModelForm
from .models import Room, User


class CreateRoomForm(ModelForm):
    # metadata
    class Meta:
        model = Room
        # fetch all editable fields
        fields = "__all__"
        exclude = ["host", "participants"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
