from django.db import models
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId

# Connect to MongoDB
client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = client[settings.MONGODB_NAME]

# MongoDB Collections
users_collection = db.users
teams_collection = db.teams
activity_collection = db.activity
leaderboard_collection = db.leaderboard
workouts_collection = db.workouts

# Model classes to help with serialization/deserialization
class User:
    def __init__(self, _id=None, username='', email='', password='', first_name='', last_name=''):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.password = password  # In production, ensure password is hashed
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def from_mongo(mongo_doc):
        return User(
            _id=mongo_doc.get('_id'),
            username=mongo_doc.get('username', ''),
            email=mongo_doc.get('email', ''),
            password=mongo_doc.get('password', ''),
            first_name=mongo_doc.get('first_name', ''),
            last_name=mongo_doc.get('last_name', '')
        )

    def to_mongo(self):
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

class Team:
    def __init__(self, _id=None, name='', description='', members=None):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.members = members or []  # List of user IDs

    @staticmethod
    def from_mongo(mongo_doc):
        return Team(
            _id=mongo_doc.get('_id'),
            name=mongo_doc.get('name', ''),
            description=mongo_doc.get('description', ''),
            members=mongo_doc.get('members', [])
        )

    def to_mongo(self):
        return {
            '_id': self._id,
            'name': self.name,
            'description': self.description,
            'members': self.members
        }

class Activity:
    def __init__(self, _id=None, user_id=None, activity_type='', duration=0, date=None, calories=0, distance=0):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.activity_type = activity_type
        self.duration = duration  # in minutes
        self.date = date
        self.calories = calories
        self.distance = distance  # in meters

    @staticmethod
    def from_mongo(mongo_doc):
        return Activity(
            _id=mongo_doc.get('_id'),
            user_id=mongo_doc.get('user_id'),
            activity_type=mongo_doc.get('activity_type', ''),
            duration=mongo_doc.get('duration', 0),
            date=mongo_doc.get('date'),
            calories=mongo_doc.get('calories', 0),
            distance=mongo_doc.get('distance', 0)
        )

    def to_mongo(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'duration': self.duration,
            'date': self.date,
            'calories': self.calories,
            'distance': self.distance
        }

class Leaderboard:
    def __init__(self, _id=None, user_id=None, score=0, rank=0, category=''):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.score = score
        self.rank = rank
        self.category = category

    @staticmethod
    def from_mongo(mongo_doc):
        return Leaderboard(
            _id=mongo_doc.get('_id'),
            user_id=mongo_doc.get('user_id'),
            score=mongo_doc.get('score', 0),
            rank=mongo_doc.get('rank', 0),
            category=mongo_doc.get('category', '')
        )

    def to_mongo(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'score': self.score,
            'rank': self.rank,
            'category': self.category
        }

class Workout:
    def __init__(self, _id=None, name='', description='', exercises=None, duration=0, difficulty='medium'):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.exercises = exercises or []
        self.duration = duration  # in minutes
        self.difficulty = difficulty

    @staticmethod
    def from_mongo(mongo_doc):
        return Workout(
            _id=mongo_doc.get('_id'),
            name=mongo_doc.get('name', ''),
            description=mongo_doc.get('description', ''),
            exercises=mongo_doc.get('exercises', []),
            duration=mongo_doc.get('duration', 0),
            difficulty=mongo_doc.get('difficulty', 'medium')
        )

    def to_mongo(self):
        return {
            '_id': self._id,
            'name': self.name,
            'description': self.description,
            'exercises': self.exercises,
            'duration': self.duration,
            'difficulty': self.difficulty
        }