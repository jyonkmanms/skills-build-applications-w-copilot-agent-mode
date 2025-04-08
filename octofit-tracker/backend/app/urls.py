from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/activities/', views.ActivityList.as_view(), name='activity-list'),
    path('api/activities/<int:pk>/', views.ActivityDetail.as_view(), name='activity-detail'),
    path('api/teams/', views.TeamList.as_view(), name='team-list'),
    path('api/teams/<int:pk>/', views.TeamDetail.as_view(), name='team-detail'),
]