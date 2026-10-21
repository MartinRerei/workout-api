
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)

    reps = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True, load_default=None)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True
    )

    @validates_schema
    def validate_workout(self, data, **kwargs):
        if data.get("duration_minutes", 0) <= 0:
            raise ValidationError(
                "Workout duration must be greater than zero.",
                field_name="duration_minutes"
            )
