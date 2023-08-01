from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# one to many relation
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # MUST reference a related name due to pre-existing user relation
    participants = models.ManyToManyField(User, related_name="participants", blank=True)

    ## snapshot every instance
    updated = models.DateField(auto_now=True)
    ## snapshot initial instance
    created = models.DateField(auto_now_add=True)

    # specify metadata
    class Meta:
        ordering = ["-updated", "-created"]

    ## return db info
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # relate a room to a message -> clear db on delete
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    # specify metadata
    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        # limit return
        return self.body[0:50]
