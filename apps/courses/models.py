import uuid
from tortoise import fields, models


class Course(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    code = fields.CharField(max_length=20, unique=True)  # e.g., CS-101
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    
    # Relationships
    instructor = fields.ForeignKeyField("models.User", related_name="courses_taught")
    students = fields.ManyToManyField(
        "models.User", 
        through="course_enrollments", 
        related_name="enrolled_courses"
    )
    
    is_published = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "courses"


class Enrollment(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    course = fields.ForeignKeyField("models.Course", related_name="enrollments")
    student = fields.ForeignKeyField("models.User", related_name="enrollments")
    enrolled_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "course_enrollments"
        unique_together = (("course", "student"),)