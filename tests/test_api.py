
import pytest

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture()
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        exercise = Exercise(
            name="Push-ups",
            category="Strength",
            equipment_needed=False,
        )
        workout = Workout(
            date=__import__("datetime").date(2026, 10, 21),
            duration_minutes=30,
            notes="Test workout",
        )

        db.session.add_all([exercise, workout])
        db.session.commit()

        db.session.add(
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercise.id,
                reps=10,
                sets=3,
            )
        )
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Workout API is running!"


def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Push-ups"


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Plank",
            "category": "Core",
            "equipment_needed": False,
        },
    )
    assert response.status_code == 201
    assert response.json["name"] == "Plank"


def test_reject_empty_exercise_name(client):
    response = client.post(
        "/exercises",
        json={
            "name": "",
            "category": "Core",
            "equipment_needed": False,
        },
    )
    assert response.status_code == 400
    assert "name" in response.json["errors"]


def test_get_workout_with_exercises(client):
    response = client.get("/workouts/1")
    assert response.status_code == 200
    assert response.json["duration_minutes"] == 30
    assert response.json["exercises"][0]["name"] == "Push-ups"


def test_reject_zero_workout_duration(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-10-21",
            "duration_minutes": 0,
            "notes": "Invalid workout",
        },
    )
    assert response.status_code == 400
    assert "duration_minutes" in response.json["errors"]


def test_missing_exercise_returns_404(client):
    response = client.get("/exercises/999")
    assert response.status_code == 404


def test_delete_exercise(client):
    response = client.delete("/exercises/1")
    assert response.status_code == 204

    missing_response = client.get("/exercises/1")
    assert missing_response.status_code == 404

def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-10-21",
            "duration_minutes": 45,
            "notes": "Leg day",
        },
    )

    assert response.status_code == 201
    assert response.json["duration_minutes"] == 45
    assert response.json["notes"] == "Leg day"


def test_add_exercise_to_workout(client):
    response = client.post(
        "/workouts/1/exercises",
        json={
            "exercise_id": 1,
            "reps": 12,
            "sets": 3,
        },
    )

    assert response.status_code == 400


def test_delete_workout(client):
    response = client.delete("/workouts/1")

    assert response.status_code == 204

    missing_response = client.get("/workouts/1")
    assert missing_response.status_code == 404

def test_add_new_exercise_to_workout(client):
    exercise = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False,
    )

    with app.app_context():
        db.session.add(exercise)
        db.session.commit()
        exercise_id = exercise.id

    response = client.post(
        "/workouts/1/exercises",
        json={
            "exercise_id": exercise_id,
            "reps": 10,
            "sets": 3,
        },
    )

    assert response.status_code == 201
    assert response.json["exercise_id"] == exercise_id
    assert response.json["reps"] == 10
    assert response.json["sets"] == 3