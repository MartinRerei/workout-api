
from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def home():
    return {"message": "Workout API is running!"}, 200


# -------------------- EXERCISES --------------------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
    except ValidationError as error:
        return {"errors": error.messages}, 400

    exercise = Exercise(**data)
    db.session.add(exercise)

    try:
        db.session.commit()
    except (IntegrityError, ValueError):
        db.session.rollback()
        return {"error": "Could not create exercise"}, 400

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not delete exercise"}, 400

    return "", 204


# -------------------- WORKOUTS --------------------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    result = workout_schema.dump(workout)
    result["exercises"] = [
        {
            **exercise_schema.dump(item.exercise),
            "reps": item.reps,
            "sets": item.sets,
            "duration_seconds": item.duration_seconds,
        }
        for item in workout.workout_exercises
    ]

    return result, 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as error:
        return {"errors": error.messages}, 400

    data.pop("workout_exercises", None)
    workout = Workout(**data)
    db.session.add(workout)

    try:
        db.session.commit()
    except (IntegrityError, ValueError):
        db.session.rollback()
        return {"error": "Could not create workout"}, 400

    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not delete workout"}, 400

    return "", 204


# -------------------- ADD EXERCISE TO WORKOUT --------------------

@app.route(
    "/workouts/<int:workout_id>/exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    try:
        data = workout_exercise_schema.load(request.get_json())
    except ValidationError as error:
        return {"errors": error.messages}, 400

    exercise = db.session.get(Exercise, data["exercise_id"])

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    association = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=data["exercise_id"],
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds"),
    )

    db.session.add(association)

    try:
        db.session.commit()
    except (IntegrityError, ValueError):
        db.session.rollback()
        return {
            "error": "Could not add exercise. Check for duplicate exercises or invalid values."
        }, 400

    return workout_exercise_schema.dump(association), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
