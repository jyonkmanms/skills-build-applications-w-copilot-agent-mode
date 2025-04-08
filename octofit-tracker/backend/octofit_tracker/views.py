from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from bson import ObjectId
from bson.errors import InvalidId

from .models import (
    User, Team, Activity, Leaderboard, Workout,
    users_collection, teams_collection, activity_collection, 
    leaderboard_collection, workouts_collection
)
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)

@api_view(['GET'])
def api_root(request, format=None):
    """
    Root API endpoint for OctoFit Tracker
    """
    base_url = request.build_absolute_uri('/').rstrip('/')
    return Response({
        'users': f"{base_url}/api/users/",
        'teams': f"{base_url}/api/teams/",
        'activity': f"{base_url}/api/activity/",
        'leaderboard': f"{base_url}/api/leaderboard/",
        'workouts': f"{base_url}/api/workouts/"
    })

class UserViewSet(APIView):
    def get(self, request, user_id=None):
        if user_id:
            try:
                user_data = users_collection.find_one({"_id": ObjectId(user_id)})
                if user_data:
                    user = User.from_mongo(user_data)
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except InvalidId:
                return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            users_data = list(users_collection.find())
            users = [User.from_mongo(user_data) for user_data in users_data]
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            users_collection.insert_one(user.to_mongo())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        try:
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            user = User.from_mongo(user_data)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = serializer.update(user, serializer.validated_data)
                users_collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": updated_user.to_mongo()}
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            result = users_collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

class TeamViewSet(APIView):
    def get(self, request, team_id=None):
        if team_id:
            try:
                team_data = teams_collection.find_one({"_id": ObjectId(team_id)})
                if team_data:
                    team = Team.from_mongo(team_data)
                    serializer = TeamSerializer(team)
                    return Response(serializer.data)
                return Response({"detail": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
            except InvalidId:
                return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            teams_data = list(teams_collection.find())
            teams = [Team.from_mongo(team_data) for team_data in teams_data]
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.create(serializer.validated_data)
            teams_collection.insert_one(team.to_mongo())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, team_id):
        try:
            team_data = teams_collection.find_one({"_id": ObjectId(team_id)})
            if not team_data:
                return Response({"detail": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
            
            team = Team.from_mongo(team_data)
            serializer = TeamSerializer(team, data=request.data, partial=True)
            if serializer.is_valid():
                updated_team = serializer.update(team, serializer.validated_data)
                teams_collection.update_one(
                    {"_id": ObjectId(team_id)},
                    {"$set": updated_team.to_mongo()}
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, team_id):
        try:
            result = teams_collection.delete_one({"_id": ObjectId(team_id)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

class ActivityViewSet(APIView):
    def get(self, request, activity_id=None):
        if activity_id:
            try:
                activity_data = activity_collection.find_one({"_id": ObjectId(activity_id)})
                if activity_data:
                    activity = Activity.from_mongo(activity_data)
                    serializer = ActivitySerializer(activity)
                    return Response(serializer.data)
                return Response({"detail": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
            except InvalidId:
                return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            activities_data = list(activity_collection.find())
            activities = [Activity.from_mongo(activity_data) for activity_data in activities_data]
            serializer = ActivitySerializer(activities, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.create(serializer.validated_data)
            activity_collection.insert_one(activity.to_mongo())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, activity_id):
        try:
            activity_data = activity_collection.find_one({"_id": ObjectId(activity_id)})
            if not activity_data:
                return Response({"detail": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
            
            activity = Activity.from_mongo(activity_data)
            serializer = ActivitySerializer(activity, data=request.data, partial=True)
            if serializer.is_valid():
                updated_activity = serializer.update(activity, serializer.validated_data)
                activity_collection.update_one(
                    {"_id": ObjectId(activity_id)},
                    {"$set": updated_activity.to_mongo()}
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, activity_id):
        try:
            result = activity_collection.delete_one({"_id": ObjectId(activity_id)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

class LeaderboardViewSet(APIView):
    def get(self, request, entry_id=None):
        if entry_id:
            try:
                entry_data = leaderboard_collection.find_one({"_id": ObjectId(entry_id)})
                if entry_data:
                    entry = Leaderboard.from_mongo(entry_data)
                    serializer = LeaderboardSerializer(entry)
                    return Response(serializer.data)
                return Response({"detail": "Leaderboard entry not found"}, status=status.HTTP_404_NOT_FOUND)
            except InvalidId:
                return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            entries_data = list(leaderboard_collection.find())
            entries = [Leaderboard.from_mongo(entry_data) for entry_data in entries_data]
            serializer = LeaderboardSerializer(entries, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = LeaderboardSerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.create(serializer.validated_data)
            leaderboard_collection.insert_one(entry.to_mongo())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, entry_id):
        try:
            entry_data = leaderboard_collection.find_one({"_id": ObjectId(entry_id)})
            if not entry_data:
                return Response({"detail": "Leaderboard entry not found"}, status=status.HTTP_404_NOT_FOUND)
            
            entry = Leaderboard.from_mongo(entry_data)
            serializer = LeaderboardSerializer(entry, data=request.data, partial=True)
            if serializer.is_valid():
                updated_entry = serializer.update(entry, serializer.validated_data)
                leaderboard_collection.update_one(
                    {"_id": ObjectId(entry_id)},
                    {"$set": updated_entry.to_mongo()}
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, entry_id):
        try:
            result = leaderboard_collection.delete_one({"_id": ObjectId(entry_id)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Leaderboard entry not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

class WorkoutViewSet(APIView):
    def get(self, request, workout_id=None):
        if workout_id:
            try:
                workout_data = workouts_collection.find_one({"_id": ObjectId(workout_id)})
                if workout_data:
                    workout = Workout.from_mongo(workout_data)
                    serializer = WorkoutSerializer(workout)
                    return Response(serializer.data)
                return Response({"detail": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)
            except InvalidId:
                return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            workouts_data = list(workouts_collection.find())
            workouts = [Workout.from_mongo(workout_data) for workout_data in workouts_data]
            serializer = WorkoutSerializer(workouts, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            workout = serializer.create(serializer.validated_data)
            workouts_collection.insert_one(workout.to_mongo())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, workout_id):
        try:
            workout_data = workouts_collection.find_one({"_id": ObjectId(workout_id)})
            if not workout_data:
                return Response({"detail": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)
            
            workout = Workout.from_mongo(workout_data)
            serializer = WorkoutSerializer(workout, data=request.data, partial=True)
            if serializer.is_valid():
                updated_workout = serializer.update(workout, serializer.validated_data)
                workouts_collection.update_one(
                    {"_id": ObjectId(workout_id)},
                    {"$set": updated_workout.to_mongo()}
                )
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workout_id):
        try:
            result = workouts_collection.delete_one({"_id": ObjectId(workout_id)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Workout not found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({"detail": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)