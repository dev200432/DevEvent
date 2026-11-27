from django.db import models

class Booking(models.Model):
    EVENT_CHOICES = [
        ('Royal Wedding', 'Royal Destination Wedding'),
        ('Corporate Gala', 'Executive Corporate Gala'),
        ('Private Party', 'VIP Private Celebration'),
        ('Product Launch', 'Brand Product Launch'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='Royal Wedding')
    event_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_type} ({self.event_date})"