import uuid
from tortoise import fields, models


class Quiz(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    course = fields.ForeignKeyField("models.Course", related_name="quizzes")
    title = fields.CharField(max_length=255)
    total_marks = fields.IntField(default=100)
    due_date = fields.DatetimeField()

    class Meta:
        table = "quizzes"


class QuizSubmission(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    quiz = fields.ForeignKeyField("models.Quiz", related_name="submissions")
    student = fields.ForeignKeyField("models.User", related_name="quiz_submissions")
    score = fields.FloatField(null=True)  # Populated after grading
    is_submitted = fields.BooleanField(default=False)
    submitted_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "quiz_submissions"
        unique_together = (("quiz", "student"),)