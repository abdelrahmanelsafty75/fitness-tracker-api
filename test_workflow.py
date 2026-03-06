import os
import sys
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client

def run_tests():
    client = Client()
    # ------ Test User Registration ------
    print("\n[1] Testing User Registration...")
    register_data = {
        "username": "abdo_hero",
        "email": "abdo@test.com",
        "password": "StrongPassword123!",
        "password_confirm": "StrongPassword123!",
        "first_name": "Abdelrhman",
        "last_name": "Elsafty"
    }
    
    res_register = client.post(
        '/api/users/register/',
        data=json.dumps(register_data),
        content_type='application/json'
    )
    if res_register.status_code == 201:
        print("User created successfully!")
    else:
        print(f"Registration failed (Maybe user already exists?): {res_register.status_code}")

    # ------ Test Login & JWT Token ------
    print("\n[2] Testing Login & JWT Token...")
    login_data = {
        "username": "abdo_hero",
        "password": "StrongPassword123!"
    }
    
    res_login = client.post(
        '/api/auth/login/',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    assert res_login.status_code == 200, "Login failed!"
    tokens = res_login.json()
    access_token = tokens['access']
    print("Login successful! Got Access Token.")

    # ------ Test Activity Creation (Protected Endpoint) ------
    print("\n[3] Testing Activity Creation (Protected Endpoint)...")
    activity_data = {
        "activity_type": "running",
        "duration": 45,
        "distance": 5.2,
        "calories_burned": 400,
        "date": str(date.today()),
        "notes": "Morning run before studying"
    }
    
    res_activity = client.post(
        '/api/activities/',
        data=json.dumps(activity_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    assert res_activity.status_code == 201, f"Activity creation failed: {res_activity.json()}"
    print("Activity logged successfully!")

    # ------ Test Fetching My Activities ------
    print("\n[4] Testing Fetching My Activities...")
    res_get_activities = client.get(
        '/api/activities/',
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )
    assert res_get_activities.status_code == 200, "Failed to fetch activities"
    response_data = res_get_activities.json()
    activities = response_data.get('results', response_data) 
    
    print(f"Fetched successfully! You have {len(activities)} activity logged.")
    if activities:
        print(f"   -> Latest Activity Details: {activities[0]['activity_type']} for {activities[0]['duration']} mins.")
    print("ALL TESTS PASSED! THE WORKFLOW IS PERFECT!")
    

if __name__ == '__main__':
    run_tests()