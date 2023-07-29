from django.db import models


class Room(models.Model):
    # host =
    # topic =
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    # participants =

    ## snapshot every instance
    updated = models.DateField(auto_now=True)
    ## snapshot initial instance
    created = models.DateField(auto_now_add=True)

    ## return db info
    def __str__(self):
        return self.name
