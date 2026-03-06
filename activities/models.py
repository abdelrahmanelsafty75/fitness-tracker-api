from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('weightlifting', 'Weightlifting'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
        help_text="Type of fitness activity"
    )

    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance in kilometers"
    )

    calories_burned = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Calories burned during activity"
    )

    date = models.DateField(help_text="Date of the activity")

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes about the activity"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"