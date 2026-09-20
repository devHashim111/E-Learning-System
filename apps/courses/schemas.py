from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from apps.auth.schemas import UserRead


class CourseBaseSchema(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    is_published: bool = False


class CourseCreateSchema(CourseBaseSchema):
    instructor_id: UUID


class CourseUpdateSchema(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    instructor_id: Optional[UUID] = None
    is_published: Optional[bool] = None


class CourseResponseSchema(CourseBaseSchema):
    id: UUID
    instructor: UserRead
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreateSchema(BaseModel):
    course_id: UUID
    student_id: UUID


class EnrollmentResponseSchema(BaseModel):
    id: UUID
    course_id: UUID
    student: UserRead
    enrolled_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)