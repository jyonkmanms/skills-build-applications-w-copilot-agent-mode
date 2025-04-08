from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout

class ObjectIdField(serializers.Field):
    """Custom serializer field for MongoDB ObjectId handling"""
    
    def to_representation(self, value):
        if value is None:
            return None
        return str(value)
    
    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))
        except (ValueError, TypeError, AttributeError):
            raise serializers.ValidationError("Invalid ObjectId format")

class UserSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def create(self, validated_data):
        return User(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        return instance

class TeamSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    members = serializers.ListField(child=ObjectIdField(), required=False)
    
    def create(self, validated_data):
        return Team(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.members = validated_data.get('members', instance.members)
        return instance

class ActivitySerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    user_id = ObjectIdField()
    activity_type = serializers.CharField(max_length=100)
    duration = serializers.IntegerField(min_value=0)  # in minutes
    date = serializers.DateTimeField(required=False)
    calories = serializers.IntegerField(min_value=0, required=False)
    distance = serializers.FloatField(min_value=0, required=False)  # in meters
    
    def create(self, validated_data):
        return Activity(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.activity_type = validated_data.get('activity_type', instance.activity_type)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.date = validated_data.get('date', instance.date)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.distance = validated_data.get('distance', instance.distance)
        return instance

class LeaderboardSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    user_id = ObjectIdField()
    score = serializers.IntegerField(min_value=0)
    rank = serializers.IntegerField(min_value=0)
    category = serializers.CharField(max_length=100, required=False)
    
    def create(self, validated_data):
        return Leaderboard(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.score = validated_data.get('score', instance.score)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.category = validated_data.get('category', instance.category)
        return instance

class WorkoutSerializer(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    exercises = serializers.ListField(child=serializers.DictField(), required=False)
    duration = serializers.IntegerField(min_value=0, required=False)  # in minutes
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard'], default='medium')
    
    def create(self, validated_data):
        return Workout(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.exercises = validated_data.get('exercises', instance.exercises)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        return instance