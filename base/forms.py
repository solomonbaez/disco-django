from django.forms import ModelForm
from .models import Room


class CreateRoomForm(ModelForm):
    # metadata
    class Meta:
        model = Room
        # fetch all editable fields
        fields = "__all__"
        exclude = ["host", "participants"]
