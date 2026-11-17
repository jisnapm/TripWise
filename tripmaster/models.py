from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TripDb(models.Model):
    title = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100)
    start_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
                                   related_name = 'trips_created')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class TripMemberDb(models.Model):
    trip = models.ForeignKey(TripDb, on_delete=models.CASCADE, related_name='trip_member')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_membership')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['trip', 'user'], name='unique_trip_member')]
        # this means the combination of trip and user must be unique

    def __str__(self):
        return f"{self.user.username} - {self.trip.title}"
