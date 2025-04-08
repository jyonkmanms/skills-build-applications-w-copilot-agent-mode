from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
import json
from bson import ObjectId
import pytest
from pymongo import MongoClient
from django.conf import settings

# We'll use pytest for testing with MongoDB

@pytest.fixture
def mongodb_client():
    """Create a MongoDB client for testing"""
    client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = client['octofit_test_db']  # Use a test database
    yield db
    # Clean up after tests
    client.drop_database('octofit_test_db')

@pytest.mark.django_db
class UserAPITests:
    """Test cases for User API endpoints"""
    
    def test_create_user(self, mongodb_client):
        """Test creating a new user"""
        client = APIClient()
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert mongodb_client.users.count_documents({}) == 1
        
    def test_get_user_list(self, mongodb_client):
        """Test retrieving user list"""
        # First create a test user
        mongodb_client.users.insert_one({
            '_id': ObjectId(),
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        
        client = APIClient()
        url = reverse('user-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class TeamAPITests:
    """Test cases for Team API endpoints"""
    
    def test_create_team(self, mongodb_client):
        """Test creating a new team"""
        client = APIClient()
        url = reverse('team-list')
        data = {
            'name': 'Test Team',
            'description': 'A team for testing',
            'members': []
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert mongodb_client.teams.count_documents({}) == 1
        
    def test_get_team_list(self, mongodb_client):
        """Test retrieving team list"""
        # First create a test team
        mongodb_client.teams.insert_one({
            '_id': ObjectId(),
            'name': 'Test Team',
            'description': 'A team for testing',
            'members': []
        })
        
        client = APIClient()
        url = reverse('team-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class ActivityAPITests:
    """Test cases for Activity API endpoints"""
    
    def test_create_activity(self, mongodb_client):
        """Test creating a new activity"""
        # First create a test user
        user_id = ObjectId()
        mongodb_client.users.insert_one({
            '_id': user_id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        client = APIClient()
        url = reverse('activity-list')
        data = {
            'user_id': str(user_id),
            'activity_type': 'Running',
            'duration': 30,
            'calories': 300,
            'distance': 5000
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert mongodb_client.activity.count_documents({}) == 1
        
    def test_get_activity_list(self, mongodb_client):
        """Test retrieving activity list"""
        # First create a test user and activity
        user_id = ObjectId()
        mongodb_client.users.insert_one({
            '_id': user_id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        mongodb_client.activity.insert_one({
            '_id': ObjectId(),
            'user_id': user_id,
            'activity_type': 'Running',
            'duration': 30,
            'calories': 300,
            'distance': 5000
        })
        
        client = APIClient()
        url = reverse('activity-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class LeaderboardAPITests:
    """Test cases for Leaderboard API endpoints"""
    
    def test_create_leaderboard_entry(self, mongodb_client):
        """Test creating a new leaderboard entry"""
        # First create a test user
        user_id = ObjectId()
        mongodb_client.users.insert_one({
            '_id': user_id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        client = APIClient()
        url = reverse('leaderboard-list')
        data = {
            'user_id': str(user_id),
            'score': 100,
            'rank': 1,
            'category': 'Running'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert mongodb_client.leaderboard.count_documents({}) == 1
        
    def test_get_leaderboard_list(self, mongodb_client):
        """Test retrieving leaderboard list"""
        # First create a test user and leaderboard entry
        user_id = ObjectId()
        mongodb_client.users.insert_one({
            '_id': user_id,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        mongodb_client.leaderboard.insert_one({
            '_id': ObjectId(),
            'user_id': user_id,
            'score': 100,
            'rank': 1,
            'category': 'Running'
        })
        
        client = APIClient()
        url = reverse('leaderboard-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class WorkoutAPITests:
    """Test cases for Workout API endpoints"""
    
    def test_create_workout(self, mongodb_client):
        """Test creating a new workout"""
        client = APIClient()
        url = reverse('workout-list')
        data = {
            'name': 'Test Workout',
            'description': 'A test workout',
            'exercises': [{'name': 'Push-ups', 'reps': 10}],
            'duration': 30,
            'difficulty': 'medium'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert mongodb_client.workouts.count_documents({}) == 1
        
    def test_get_workout_list(self, mongodb_client):
        """Test retrieving workout list"""
        # First create a test workout
        mongodb_client.workouts.insert_one({
            '_id': ObjectId(),
            'name': 'Test Workout',
            'description': 'A test workout',
            'exercises': [{'name': 'Push-ups', 'reps': 10}],
            'duration': 30,
            'difficulty': 'medium'
        })
        
        client = APIClient()
        url = reverse('workout-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1