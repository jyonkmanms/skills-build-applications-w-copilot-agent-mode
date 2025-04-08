from django.shortcuts import render
from rest_framework import viewsets
from .models import Activity, UserProfile
from .serializers import ActivitySerializer, UserProfileSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

def home(request):
    return render(request, 'index.html')