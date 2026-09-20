from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from apps.auth.schemas import UserRead


class QuizBaseSchema(BaseModel):
    title: str
    total_marks: int = 100
    due_date: datetime


class QuizCreateSchema(QuizBaseSchema):
    course_id: UUID


class QuizUpdateSchema(BaseModel):
    title: Optional[str] = None
    total_marks: Optional[int] = None
    due_date: Optional[datetime] = None


class QuizResponseSchema(QuizBaseSchema):
    id: UUID
    course_id: UUID

    model_config = ConfigDict(from_attributes=True)


class QuizSubmissionCreateSchema(BaseModel):
    quiz_id: UUID


class QuizGradeSchema(BaseModel):
    score: float


class QuizSubmissionResponseSchema(BaseModel):
    id: UUID
    quiz_id: UUID
    student: UserRead
    score: Optional[float] = None
    is_submitted: bool
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)