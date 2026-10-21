# Workout Application Backend API

A RESTful API built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow for managing exercises, workouts, and the exercises associated with each workout.

## Features

- Create, retrieve, and delete exercises.
- Retrieve individual exercises.
- Create, retrieve, and delete workouts.
- Retrieve a workout with its associated exercises.
- Add exercises to existing workouts.
- Validate incoming request data using Marshmallow.
- Enforce data integrity using SQLAlchemy models and database constraints.
- Manage database migrations with Flask-Migrate.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pytest
- Pipenv

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd workout-api
```

Replace the placeholder URL with your actual GitHub repository URL.

### 2. Install dependencies

```bash
python -m pipenv install --dev
```

### 3. Initialize the database

```bash
python -m pipenv run flask --app server.app db upgrade
```

### 4. Seed sample data

```bash
python -m pipenv run python -m server.seed
```

## Running the Application

Start the development server:

```bash
python -m pipenv run python server/app.py
```

The API runs at:

`http://127.0.0.1:5555`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<workout_id>` | Retrieve a workout and its exercises |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |
| POST | `/workouts/<workout_id>/exercises` | Add an exercise to a workout |

## Example Requests

### Create an exercise

`POST /exercises`

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

### Create a workout

`POST /workouts`

```json
{
  "date": "2026-10-21",
  "duration_minutes": 30,
  "notes": "Full-body workout"
}
```

### Add an exercise to a workout

`POST /workouts/1/exercises`

```json
{
  "exercise_id": 1,
  "reps": 10,
  "sets": 3
}
```

## Running Tests

Run the automated test suite:

```bash
python -m pipenv run python -m pytest -v
```

## Error Handling

The API returns appropriate HTTP status codes, including:

- `200 OK` — Successful retrieval.
- `201 Created` — Resource created successfully.
- `204 No Content` — Resource deleted successfully.
- `400 Bad Request` — Invalid input or operation rejected.
- `404 Not Found` — Requested resource does not exist.

## Database Migrations

Apply existing migrations:

```bash
python -m pipenv run flask --app server.app db upgrade
```

Generate a new migration after model changes:

```bash
python -m pipenv run flask --app server.app db migrate -m "Describe the change"
```

## License

Add your chosen project license here if required.
