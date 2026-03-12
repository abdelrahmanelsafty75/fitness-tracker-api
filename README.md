<div align="center">

# Fitness Tracker API

A secure, fully-featured REST API for logging and analyzing fitness activities — built with Django and Django REST Framework.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red?style=flat-square)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens)](https://django-rest-framework-simplejwt.readthedocs.io)
[![Live](https://img.shields.io/badge/Live-PythonAnywhere-1DA462?style=flat-square)](https://elsafty.pythonanywhere.com/api/schema/swagger-ui/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Base URL:** `https://elsafty.pythonanywhere.com`

</div>

---

## Overview

The Fitness Tracker API allows authenticated users to record workout sessions, query their history with advanced filtering, and retrieve aggregated analytics — including activity summaries, weekly/monthly trends, and per-type statistics. All data is user-scoped; users can only access their own records.


---

## Tech Stack

| Concern | Technology |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Django 6.0.3 |
| API Framework | Django REST Framework 3.16.1 |
| Authentication | JWT — `djangorestframework-simplejwt` |
| Filtering | `django-filter` |
| API Documentation | `drf-spectacular` (OpenAPI 3, Swagger UI, ReDoc) |
| Database | SQLite (development) / PostgreSQL (production) |
| Hosting | PythonAnywhere |

---

## Project Structure

```
fitness-tracker-api/
├── activities/          # Activity model, serializers, views, filters
├── users/               # User registration and profile management
├── config/              # Settings, root URL config, WSGI/ASGI
├── test_workflow.py     # End-to-end integration tests
├── requirements.txt
├── build.sh
└── manage.py
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/abdelrahmanelsafty75/fitness-tracker-api.git
cd fitness-tracker-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# (Optional) Create an admin account
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API is available locally at `http://127.0.0.1:8000/`.

---

## Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

> Never commit `.env` to version control. Ensure it is listed in `.gitignore`.

---

## API Reference

All endpoints are prefixed with `/api/`.  
Protected endpoints require the header: `Authorization: Bearer <access_token>`

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| POST | `/api/auth/login/` | Obtain JWT access and refresh tokens | No |
| POST | `/api/auth/refresh/` | Refresh an expired access token | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| POST | `/api/users/register/` | Register a new user account | No |
| GET | `/api/users/<id>/` | Retrieve a user's profile | Yes |
| PUT / PATCH | `/api/users/profile/` | Update the authenticated user's profile | Yes |
| GET | `/api/users/list/` | List all users | Admin only |

### Activities

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/api/activities/` | List activities (supports filtering) | Yes |
| POST | `/api/activities/` | Create a new activity | Yes |
| GET | `/api/activities/<id>/` | Retrieve a single activity | Yes |
| PUT / PATCH | `/api/activities/<id>/` | Update an activity | Owner only |
| DELETE | `/api/activities/<id>/` | Delete an activity | Owner only |
| GET | `/api/activities/summary/` | Aggregated totals and averages | Yes |
| GET | `/api/activities/trends/` | Weekly or monthly trend data | Yes |
| GET | `/api/activities/stats-by-type/` | Statistics grouped by activity type | Yes |


---

## Interactive Documentation

Three documentation interfaces are auto-generated via `drf-spectacular`:

| Interface | URL |
|-----------|-----|
| Swagger UI | [elsafty.pythonanywhere.com/api/docs/swagger/](https://elsafty.pythonanywhere.com/api/docs/swagger/) |
| ReDoc | [elsafty.pythonanywhere.com/api/docs/redoc/](https://elsafty.pythonanywhere.com/api/docs/redoc/) |
| OpenAPI Schema | [elsafty.pythonanywhere.com/api/schema/](https://elsafty.pythonanywhere.com/api/schema/) |

**Authenticating in Swagger UI:**
1. Call `POST /api/auth/login/` to retrieve your access token
2. Click **Authorize** (top right)
3. Enter `Bearer <your_access_token>`
4. All protected endpoints are now accessible

---

## Testing

```bash
python test_workflow.py
```

Covers the following scenarios:

- User registration and login
- Activity CRUD operations
- Filtering, sorting, and pagination
- Summary, trends, and stats-by-type responses
- Permission enforcement (owner-only access)

---

## Deployment

### JWT Token Settings

| Setting | Value |
|---------|-------|
| Access token lifetime | 60 minutes |
| Refresh token lifetime | 1 day |
| Token prefix | `Bearer` |

### PythonAnywhere

1. Upload your code via the **Files** tab or `git clone` in a Bash console
2. Create a virtual environment and run `pip install -r requirements.txt`
3. Run `python manage.py migrate`
4. Configure the WSGI file to point to `config.wsgi`
5. Set environment variables under the **Web** tab → *Environment variables*
6. Reload the web app

---


## Author

**Abdelrhman Elsafty**

- GitHub: [github.com/abdelrahmanelsafty75](https://github.com/abdelrahmanelsafty75)
- LinkedIn: [linkedin.com/in/abdelrahmanelsafty75](https://www.linkedin.com/in/abdelrahmanelsafty75)
- Email: abdelrhmanelsafty74@gmail.com

---

*Licensed under the MIT License.*