# Fitness Tracker API

A comprehensive Fitness Tracker API built with Django and Django REST Framework. This API allows users to manage their fitness activities by logging, updating, deleting, and viewing their activity history with detailed metrics and analytics.

## Features

### Core Features
- **User Management**: Registration, login, profile management with JWT authentication
- **Activity CRUD**: Create, Read, Update, Delete fitness activities
- **Activity Types**: Running, Cycling, Weightlifting, Swimming, Walking, Yoga, HIIT, Other
- **Data Tracking**: Duration, Distance, Calories Burned, Date, Notes
- **Security**: Users can only access and modify their own activities

### Advanced Features
- **Filtering**: By activity type, date range, duration, calories
- **Sorting**: By date, duration, calories burned
- **Pagination**: Configurable page sizes for large datasets
- **Activity Summary**: Total statistics (duration, distance, calories)
- **Activity Trends**: Weekly and monthly trend analysis
- **Stats by Type**: Breakdown of activities by type

## Tech Stack

- **Framework**: Django 6.0.3
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (JSON Web Tokens) via djangorestframework-simplejwt
- **Filtering**: django-filter
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/abdelrahmanelsafty75/fitness-tracker-api.git
   cd fitness-tracker-api
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-filter
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Obtain JWT access and refresh tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/register/` | Register a new user | No |
| PUT/PATCH | `/api/users/profile/` | Update user profile | Yes |
| GET | `/api/users/list/` | List all users (admin only) | Yes (Admin) |
| GET | `/api/users/<id>/` | Get specific user details | Yes |

### Activities

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/activities/` | List all activities (with filters) | Yes |
| POST | `/api/activities/` | Create a new activity | Yes |
| GET | `/api/activities/<id>/` | Get specific activity | Yes |
| PUT/PATCH | `/api/activities/<id>/` | Update an activity | Yes (Owner only) |
| DELETE | `/api/activities/<id>/` | Delete an activity | Yes (Owner only) |
| GET | `/api/activities/summary/` | Get activity summary statistics | Yes |
| GET | `/api/activities/trends/` | Get activity trends (weekly/monthly) | Yes |
| GET | `/api/activities/stats-by-type/` | Get statistics grouped by activity type | Yes |

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login (Get JWT Token)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Create an Activity

```bash
curl -X POST http://127.0.0.1:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-access-token>" \
  -d '{
    "activity_type": "running",
    "duration": 30,
    "distance": 5.5,
    "calories_burned": 300,
    "date": "2026-03-05",
    "notes": "Morning run in the park"
  }'
```

**Response:**
```json
{
  "id": 1,
  "user": "johndoe",
  "activity_type": "running",
  "duration": 30,
  "distance": "5.50",
  "calories_burned": 300,
  "date": "2026-03-05",
  "notes": "Morning run in the park",
  "created_at": "2026-03-05T10:00:00.000000Z",
  "updated_at": "2026-03-05T10:00:00.000000Z"
}
```

### 4. List Activities with Filters

```bash
# Filter by activity type
curl -X GET "http://127.0.0.1:8000/api/activities/?activity_type=running" \
  -H "Authorization: Bearer <your-access-token>"

# Filter by date range
curl -X GET "http://127.0.0.1:8000/api/activities/?start_date=2026-03-01&end_date=2026-03-31" \
  -H "Authorization: Bearer <your-access-token>"

# Sort by duration (ascending)
curl -X GET "http://127.0.0.1:8000/api/activities/?ordering=duration" \
  -H "Authorization: Bearer <your-access-token>"

# Sort by date (descending - newest first)
curl -X GET "http://127.0.0.1:8000/api/activities/?ordering=-date" \
  -H "Authorization: Bearer <your-access-token>"
```

### 5. Get Activity Summary

```bash
curl -X GET "http://127.0.0.1:8000/api/activities/summary/" \
  -H "Authorization: Bearer <your-access-token>"
```

**Response:**
```json
{
  "total_activities": 10,
  "total_duration": 450,
  "total_distance": 85.5,
  "total_calories": 3500,
  "average_duration": 45.0
}
```

### 6. Get Activity Trends

```bash
# Weekly trends
curl -X GET "http://127.0.0.1:8000/api/activities/trends/?period=weekly" \
  -H "Authorization: Bearer <your-access-token>"

# Monthly trends
curl -X GET "http://127.0.0.1:8000/api/activities/trends/?period=monthly" \
  -H "Authorization: Bearer <your-access-token>"
```

**Response:**
```json
[
  {
    "period": "2026-03-02",
    "total_duration": 160,
    "total_distance": 24.5,
    "total_calories": 1200,
    "activity_count": 4
  }
]
```

### 7. Get Stats by Activity Type

```bash
curl -X GET "http://127.0.0.1:8000/api/activities/stats-by-type/" \
  -H "Authorization: Bearer <your-access-token>"
```

**Response:**
```json
[
  {
    "activity_type": "running",
    "total_activities": 5,
    "total_duration": 150,
    "total_distance": 25.0,
    "total_calories": 1500,
    "average_duration": 30.0
  },
  {
    "activity_type": "cycling",
    "total_activities": 3,
    "total_duration": 135,
    "total_distance": 45.0,
    "total_calories": 1200,
    "average_duration": 45.0
  }
]
```

## Query Parameters

### Activity List Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `activity_type` | string | Filter by activity type (running, cycling, etc.) |
| `start_date` | date | Filter activities from this date (YYYY-MM-DD) |
| `end_date` | date | Filter activities up to this date (YYYY-MM-DD) |
| `min_duration` | integer | Minimum duration in minutes |
| `max_duration` | integer | Maximum duration in minutes |
| `min_calories` | integer | Minimum calories burned |
| `max_calories` | integer | Maximum calories burned |
| `ordering` | string | Sort by field (prefix with `-` for descending) |
| `page` | integer | Page number for pagination |
| `page_size` | integer | Number of results per page |

### Activity Summary Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start_date` | date | Start date for summary period |
| `end_date` | date | End date for summary period |

### Activity Trends Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `period` | string | `weekly` or `monthly` (default: weekly) |

## Activity Types

The following activity types are supported:

- `running` - Running
- `cycling` - Cycling
- `weightlifting` - Weightlifting
- `swimming` - Swimming
- `walking` - Walking
- `yoga` - Yoga
- `hiit` - High-Intensity Interval Training
- `other` - Other activities

## Data Models

### User Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `username` | string | Unique username |
| `email` | string | Unique email address |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `created_at` | datetime | Account creation timestamp |
| `updated_at` | datetime | Last update timestamp |

### Activity Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier |
| `user` | foreign key | User who created the activity |
| `activity_type` | string | Type of activity |
| `duration` | integer | Duration in minutes |
| `distance` | decimal | Distance in kilometers (optional) |
| `calories_burned` | integer | Calories burned (optional) |
| `date` | date | Date of activity |
| `notes` | text | Additional notes (optional) |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

## Testing

Run the test script to verify all API functionality:

```bash
python test_workflow.py
```

This will test:
- User registration and login
- Activity CRUD operations
- Filtering and sorting
- Pagination
- Summary and trends endpoints
- Permission checks

## Configuration

### JWT Settings

JWT tokens are configured with the following settings:

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 1 day
- **Token Type**: Bearer

### Pagination

Default pagination settings:

- **Page Size**: 10 items per page
- **Max Page Size**: 100 items

### Database

By default, the project uses SQLite. To use PostgreSQL or MySQL, update the `DATABASES` setting in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fitness_tracker',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login
2. Create a `Procfile`:
   ```
   web: gunicorn fitness_tracker.wsgi
   ```
3. Add `gunicorn` to requirements.txt
4. Set environment variables:
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

### PythonAnywhere Deployment

1. Upload your code to PythonAnywhere
2. Create a virtual environment and install dependencies
3. Configure the WSGI file
4. Set up the database
5. Collect static files

## Security Features

- JWT-based authentication
- Password validation (minimum length, common passwords check)
- Users can only access their own data
- CSRF protection for session-based authentication
- Secure password hashing (PBKDF2 by default)

## Future Enhancements

Potential features to add:

- **Goal Setting**: Set and track fitness goals
- **Workout Plans**: Create multi-activity workout routines
- **Social Features**: Share activities, leaderboards
- **Notifications**: Reminders and achievement alerts
- **Wearable Integration**: Connect with fitness devices
- **Export Data**: CSV/Excel export functionality

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.




##  Contact
For questions, suggestions, or collaboration:


#### Author: Abdelrhman Elsafty


- GitHub: @abdelrahmanelsafty75

- Email: abdelrhmanelsafty74gmail.com

- LinkedIn: www.linkedin.com/in/abdelrahmanelsafty75


