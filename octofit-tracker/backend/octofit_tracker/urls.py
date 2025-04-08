from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root, name='api-root'),  # Root API endpoint
    path('api/users/', views.UserViewSet.as_view(), name='user-list'),
    path('api/users/<str:user_id>/', views.UserViewSet.as_view(), name='user-detail'),
    path('api/teams/', views.TeamViewSet.as_view(), name='team-list'),
    path('api/teams/<str:team_id>/', views.TeamViewSet.as_view(), name='team-detail'),
    path('api/activities/', views.ActivityViewSet.as_view(), name='activity-list'),
    path('api/activities/<str:activity_id>/', views.ActivityViewSet.as_view(), name='activity-detail'),
    path('api/leaderboard/', views.LeaderboardViewSet.as_view(), name='leaderboard-list'),
    path('api/leaderboard/<str:entry_id>/', views.LeaderboardViewSet.as_view(), name='leaderboard-detail'),
    path('api/workouts/', views.WorkoutViewSet.as_view(), name='workout-list'),
    path('api/workouts/<str:workout_id>/', views.WorkoutViewSet.as_view(), name='workout-detail'),
]

# Add format suffix patterns for API responses
urlpatterns = format_suffix_patterns(urlpatterns)