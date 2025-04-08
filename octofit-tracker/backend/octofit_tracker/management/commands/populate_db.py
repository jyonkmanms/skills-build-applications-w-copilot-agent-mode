from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.models import users_collection, teams_collection, activity_collection, leaderboard_collection, workouts_collection
from datetime import datetime, timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # First, drop all indexes to avoid conflicts
        self.stdout.write('Dropping existing indexes...')
        try:
            activity_collection.drop_indexes()
            leaderboard_collection.drop_indexes()
            workouts_collection.drop_indexes()
            teams_collection.drop_indexes()
            users_collection.drop_indexes()
            self.stdout.write('Successfully dropped collection indexes')
        except Exception as e:
            self.stdout.write(f'Error dropping indexes: {e}')
        
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Clear existing collections
        self.stdout.write('Clearing existing collections...')
        users_collection.delete_many({})
        teams_collection.delete_many({})
        activity_collection.delete_many({})
        leaderboard_collection.delete_many({})
        workouts_collection.delete_many({})
        
        # Create users
        self.stdout.write('Creating users...')
        user_ids = self.create_users()
        
        # Create teams
        self.stdout.write('Creating teams...')
        self.create_teams(user_ids)
        
        # Create activities
        self.stdout.write('Creating activities...')
        self.create_activities(user_ids)
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        self.create_leaderboard(user_ids)
        
        # Create workouts
        self.stdout.write('Creating workouts...')
        self.create_workouts()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data!'))
    
    def create_users(self):
        users = [
            User(username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword', 
                 first_name='Thor', last_name='Odinson'),
            User(username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword', 
                 first_name='Tony', last_name='Stark'),
            User(username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword', 
                 first_name='Dade', last_name='Murphy'),
            User(username='crashoverride', email='crashoverride@mhigh.edu', password='crashoverridepassword', 
                 first_name='Zero', last_name='Cool'),
            User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword', 
                 first_name='Sleep', last_name='Token')
        ]
        
        user_ids = []
        for user in users:
            mongo_doc = user.to_mongo()
            users_collection.insert_one(mongo_doc)
            user_ids.append(mongo_doc['_id'])
            self.stdout.write(f"Created user: {user.username}")
        
        return user_ids
    
    def create_teams(self, user_ids):
        teams = [
            Team(name='Blue Team', description='The Blue Team', members=[user_ids[0], user_ids[2]]),
            Team(name='Gold Team', description='The Gold Team', members=[user_ids[1], user_ids[3], user_ids[4]])
        ]
        
        for team in teams:
            mongo_doc = team.to_mongo()
            # Add a unique team_id
            mongo_doc['team_id'] = str(ObjectId())
            teams_collection.insert_one(mongo_doc)
            self.stdout.write(f"Created team: {team.name}")
    
    def create_activities(self, user_ids):
        # Using full datetime objects instead of date objects for MongoDB compatibility
        today = datetime.now()
        
        activities = []
        activity_types = ['CYCLING', 'WEIGHTLIFTING', 'RUNNING', 'YOGA', 'SWIMMING']
        durations = [60, 120, 90, 30, 75]
        calories = [500, 700, 800, 200, 600]
        distances = [20000, 0, 10000, 0, 3000]
        
        for i, user_id in enumerate(user_ids):
            # Create a custom activity_id for each activity to avoid duplicates
            activity_id = str(ObjectId())
            
            activity = Activity(
                user_id=user_id, 
                activity_type=activity_types[i % len(activity_types)], 
                duration=durations[i % len(durations)], 
                date=today - timedelta(days=5-i), 
                calories=calories[i % len(calories)], 
                distance=distances[i % len(distances)]
            )
            
            # Add the activity_id to the mongo document directly
            mongo_doc = activity.to_mongo()
            mongo_doc['activity_id'] = activity_id
            
            activity_collection.insert_one(mongo_doc)
            self.stdout.write(f"Created activity: {activity.activity_type} for user {activity.user_id}")
    
    def create_leaderboard(self, user_ids):
        categories = ['OVERALL', 'OVERALL', 'OVERALL', 'OVERALL', 'OVERALL',
                      'CYCLING', 'WEIGHTLIFTING', 'RUNNING', 'YOGA', 'SWIMMING']
        scores = [100, 90, 95, 85, 80, 95, 98, 92, 88, 94]
        ranks = [1, 2, 3, 4, 5, 1, 1, 1, 1, 1]
        
        for i, (category, score, rank) in enumerate(zip(categories, scores, ranks)):
            user_id = user_ids[i % len(user_ids)]
            
            leaderboard_entry = Leaderboard(
                user_id=user_id,
                score=score,
                rank=rank,
                category=category
            )
            
            # Add a unique leaderboard_id
            mongo_doc = leaderboard_entry.to_mongo()
            mongo_doc['leaderboard_id'] = str(ObjectId())
            
            leaderboard_collection.insert_one(mongo_doc)
            self.stdout.write(f"Created leaderboard entry: {category} rank {rank} for user {user_id}")
    
    def create_workouts(self):
        workout_data = [
            {
                'name': 'Cycling Training',
                'description': 'Training for a road cycling event',
                'exercises': ['Warm-up ride', 'Sprint intervals', 'Hill climbs', 'Cool down'],
                'duration': 60,
                'difficulty': 'medium'
            },
            {
                'name': 'Crossfit',
                'description': 'Training for a crossfit competition',
                'exercises': ['Burpees', 'Pull-ups', 'Push-ups', 'Box jumps', 'Kettlebell swings'],
                'duration': 90,
                'difficulty': 'hard'
            },
            {
                'name': 'Running Training',
                'description': 'Training for a marathon',
                'exercises': ['Warm-up jog', 'Speed work', 'Long distance', 'Recovery', 'Cool down'],
                'duration': 120,
                'difficulty': 'medium'
            },
            {
                'name': 'Strength Training',
                'description': 'Training for strength',
                'exercises': ['Squats', 'Deadlifts', 'Bench press', 'Shoulder press', 'Rows'],
                'duration': 45,
                'difficulty': 'hard'
            },
            {
                'name': 'Swimming Training',
                'description': 'Training for a swimming competition',
                'exercises': ['Warm-up laps', 'Freestyle drills', 'Backstroke drills', 'Endurance work', 'Cool down'],
                'duration': 75,
                'difficulty': 'medium'
            }
        ]
        
        for data in workout_data:
            workout = Workout(**data)
            
            # Add a unique workout_id
            mongo_doc = workout.to_mongo()
            mongo_doc['workout_id'] = str(ObjectId())
            
            workouts_collection.insert_one(mongo_doc)
            self.stdout.write(f"Created workout: {workout.name}")