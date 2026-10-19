from django.db import models


class Event(models.Model):

    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('concert', 'Concert'),
        ('sports', 'Sports'),
        ('party', 'Party'),
        ('other', 'Other'),
    ]

    event_name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    description = models.TextField()

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    location = models.CharField(max_length=250)

    organizer = models.CharField(max_length=150)

    ticket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    max_participants = models.PositiveIntegerField(default=100)

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


class EventReview(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='event_reviews'
    )

    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )

    comment = models.TextField(
        max_length=1000,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'user'],
                name='unique_event_review_per_user'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.event.event_name} ({self.rating}/5)'


    def __str__(self):
        return self.event_name