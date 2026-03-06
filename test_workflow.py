import os
import sys
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client

def run_full_tests():
    client = Client()
    print("\n" + "=" * 55)
    print("FITNESS TRACKER API - FULL WORKFLOW TEST ")
    print("=" * 55)

    # ------ [1] Test User Registration ------
    print("\n[1] Testing User Registration...")
    register_data = {
        "username": "abdo_hero_2",
        "email": "abdo2@test.com",
        "password": "StrongPassword123!",
        "password_confirm": "StrongPassword123!",
        "first_name": "Abdelrhman",
        "last_name": "Elsafty"
    }
    res_register = client.post('/api/users/register/', data=json.dumps(register_data), content_type='application/json')
    if res_register.status_code == 201:
        print("User created successfully!")
    else:
        print(f"Registration skipped (User might exist). Status: {res_register.status_code}")

    # ------ [2] Test Login & JWT Token ------
    print("\n[2] Testing Login & JWT Token...")
    login_data = {"username": "abdo_hero_2", "password": "StrongPassword123!"}
    res_login = client.post('/api/auth/login/', data=json.dumps(login_data), content_type='application/json')
    assert res_login.status_code == 200, "Login failed!"
    access_token = res_login.json()['access']
    headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
    print("Login successful! Got Access Token.")

    # ------ [3] Test Activity Creation ------
    print("\n[3] Testing Activity Creation...")
    activities_to_create = [
        {"activity_type": "running", "duration": 45, "distance": 5.0, "calories_burned": 400, "date": str(date.today())},
        {"activity_type": "weightlifting", "duration": 60, "calories_burned": 350, "date": str(date.today())}
    ]
    for act in activities_to_create:
        res_act = client.post('/api/activities/', data=json.dumps(act), content_type='application/json', **headers)
        assert res_act.status_code == 201, f"Activity creation failed: {res_act.json()}"
    print(f"Created {len(activities_to_create)} activities successfully!")

    # ------ [4] Test Filters ------
    print("\n[4] Testing Filters (?activity_type=running)...")
    res_filter = client.get('/api/activities/?activity_type=running', **headers)
    assert res_filter.status_code == 200, "Filter failed"
    running_count = res_filter.json().get('count', 0)
    print(f"Filter working! Found {running_count} running activities.")

    # ------ [5] Test Summary Analytics ------
    print("\n[5] Testing Summary Analytics (/api/activities/summary/)...")
    res_summary = client.get('/api/activities/summary/', **headers)
    assert res_summary.status_code == 200, "Summary failed"
    print("Summary Data:")
    print(json.dumps(res_summary.json(), indent=2))

    # ------ [6] Test Stats by Type ------
    print("\n[6] Testing Stats by Type (/api/activities/stats-by-type/)...")
    res_stats = client.get('/api/activities/stats-by-type/', **headers)
    assert res_stats.status_code == 200, "Stats failed"
    print("Stats Data:")
    print(json.dumps(res_stats.json(), indent=2))

    print("\n" + "=" * 55)
    print("ALL TESTS PASSED!")
    print("=" * 55 + "\n")

if __name__ == '__main__':
    run_full_tests()