
from datetime import date

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise


def seed_data():
    with app.app_context():
        # Create the database tables if they do not exist.
        db.create_all()

        # Avoid duplicating the sample data when the script is run again.
        if Exercise.query.first() or Workout.query.first():
            print("Database already contains data. Skipping seed.")
            return

        exercises = [
            Exercise(
                name="Push-ups",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Squats",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Treadmill Running",
                category="Cardio",
                equipment_needed=True
            ),
            Exercise(
                name="Dumbbell Rows",
                category="Strength",
                equipment_needed=True
            ),
        ]

        db.session.add_all(exercises)
        db.session.flush()

        workout = Workout(
            date=date.today(),
            duration_minutes=45,
            notes="Full-body workout"
        )

        db.session.add(workout)
        db.session.flush()

        workout_exercises = [
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercises[0].id,
                reps=15,
                sets=3
            ),
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercises[1].id,
                reps=12,
                sets=3
            ),
            WorkoutExercise(
                workout_id=workout.id,
                exercise_id=exercises[2].id,
                duration_seconds=600
            ),
        ]

        db.session.add_all(workout_exercises)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Exercises created: {len(exercises)}")
        print("Workouts created: 1")
        print(f"Workout-exercise records created: {len(workout_exercises)}")


if __name__ == "__main__":
    seed_data()
