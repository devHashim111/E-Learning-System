from fastapi import HTTPException
from fapix.views import ModelViewSet
from fapix.decorators import action
from apps.auth.permissions import IsAuthenticated, IsSuperUserOrRole
from .models import Course, Enrollment
from .schemas import (
    CourseResponseSchema,
    CourseCreateSchema,
    CourseUpdateSchema,
    EnrollmentResponseSchema,
    EnrollmentCreateSchema,
)


class CourseViewSet(ModelViewSet):
    model = Course
    schema = CourseResponseSchema
    
    action_schemas = {
        "create": CourseCreateSchema,
        "update": CourseUpdateSchema,
        "partial_update": CourseUpdateSchema,
    }

    permission_classes = [IsAuthenticated]
    action_permissions = {
        "create": [IsSuperUserOrRole("admin", "teacher", "supervisor")],
        "update": [IsSuperUserOrRole("admin", "teacher")],
        "destroy": [IsSuperUserOrRole("admin")],
    }

    search_fields = ["code", "title", "description"]
    filterset_fields = ["is_published", "instructor_id"]
    ordering_fields = ["created_at", "code"]
    default_ordering = ["-created_at"]

    def get_queryset(self):
        """Pre-fetch related foreign keys to allow Pydantic serialization."""
        return self.model.all().select_related("instructor")

    @action(detail=True, methods=["POST"], schema=EnrollmentCreateSchema)
    async def enroll_student(self, request, pk=None):
        course = await self.get_object(pk)
        
        data = await request.json()
        student_id = data.get("student_id")

        enrollment, created = await Enrollment.get_or_create(
            course_id=course.id,
            student_id=student_id,
        )
        if not created and not enrollment.is_active:
            enrollment.is_active = True
            await enrollment.save()

        return {"status": "success", "message": "Student successfully enrolled", "course_id": str(course.id)}


class EnrollmentViewSet(ModelViewSet):
    model = Enrollment
    schema = EnrollmentResponseSchema
    action_schemas = {"create": EnrollmentCreateSchema}

    permission_classes = [IsAuthenticated]
    action_permissions = {
        "create": [IsSuperUserOrRole("admin", "teacher", "supervisor")],  # Added supervisor
        "destroy": [IsSuperUserOrRole("admin", "teacher")],
    }

    filterset_fields = ["course_id", "student_id", "is_active"]

    def get_queryset(self):
        """Pre-fetch related foreign keys to allow Pydantic serialization."""
        return self.model.all().select_related("course", "student")