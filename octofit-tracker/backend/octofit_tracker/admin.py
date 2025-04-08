from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout

# Note: Since we're using MongoDB directly and not Django's ORM,
# we won't use the standard Django admin site registration.
# Instead, we'll create custom admin views if needed.

# This is a placeholder for future admin site customization
# For a production app, you might want to implement custom admin views
# that interact with MongoDB directly.

class MongoDBModelAdmin(admin.ModelAdmin):
    """
    Base admin class for MongoDB models
    This is a placeholder implementation and would need customization
    for a production environment
    """
    
    def get_queryset(self, request):
        # This is just a placeholder to prevent errors in Django admin
        return []
    
    def has_add_permission(self, request):
        # Disable add through Django admin for MongoDB models
        return False
    
    def has_change_permission(self, request, obj=None):
        # Disable change through Django admin for MongoDB models
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Disable delete through Django admin for MongoDB models
        return False