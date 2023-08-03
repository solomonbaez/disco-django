from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Room


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
        fields = ["email", "name", "username", "bio", "avatar"]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        # password1/password2 == password/conf
        fields = ["email", "name", "username", "password1", "password2"]
