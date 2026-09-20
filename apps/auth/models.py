import uuid
from enum import Enum
from tortoise import fields, models


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    SUPERVISOR = "supervisor"  # Principal / Dept Head
    ADMIN = "admin"


class User(models.Model):
    """
    Core authentication model with RBAC support for LMS.
    """
    
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=150, unique=True, null=True)
    hashed_password = fields.CharField(max_length=255)
    
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)

    is_active = fields.BooleanField(default=True)
    is_verified = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    role = fields.CharField(
        max_length=50,
        default=UserRole.STUDENT.value,
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "auth_users"

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_teacher(self) -> bool:
        return self.role == UserRole.TEACHER.value

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT.value

    @property
    def is_supervisor(self) -> bool:
        return self.role == UserRole.SUPERVISOR.value