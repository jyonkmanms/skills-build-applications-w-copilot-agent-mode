from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Activity(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()  # Duration in minutes
    distance = models.FloatField(null=True, blank=True)  # Distance in kilometers
    date = models.DateField()

    def __str__(self):
        return f"{self.activity_type} by {self.user.username} on {self.date}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.TextField()

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.badge.name} awarded to {self.user.username}"