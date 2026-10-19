from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class  Registration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
         on_delete=models.CASCADE
         )
    
    event = models.ForeignKey(
        Event,
         on_delete=models.CASCADE
         )
    
    registration_date = models.DateTimeField(
        auto_now_add=True
        )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )
    def __str__(self):
        return f"{self.user.username} - {self.event.event_name}"