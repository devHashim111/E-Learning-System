from fastapi import HTTPException
from fapix.views import ModelViewSet
from fapix.decorators import action
from apps.auth.permissions import IsAuthenticated, IsSuperUserOrRole
from .models import Quiz, QuizSubmission
from .schemas import (
    QuizResponseSchema,
    QuizCreateSchema,
    QuizUpdateSchema,
    QuizSubmissionResponseSchema,
    QuizSubmissionCreateSchema,
    QuizGradeSchema,
)


class QuizViewSet(ModelViewSet):
    model = Quiz
    schema = QuizResponseSchema
    
    action_schemas = {
        "create": QuizCreateSchema,
        "update": QuizUpdateSchema,
        "partial_update": QuizUpdateSchema,
    }

    permission_classes = [IsAuthenticated]
    action_permissions = {
        "create": [IsSuperUserOrRole("admin", "teacher")],
        "update": [IsSuperUserOrRole("admin", "teacher")],
        "destroy": [IsSuperUserOrRole("admin", "teacher")],
    }

    filterset_fields = ["course_id"]
    search_fields = ["title"]


class QuizSubmissionViewSet(ModelViewSet):
    model = QuizSubmission
    schema = QuizSubmissionResponseSchema
    action_schemas = {"create": QuizSubmissionCreateSchema}

    permission_classes = [IsAuthenticated]
    action_permissions = {
        "create": [IsSuperUserOrRole("student")],
    }

    filterset_fields = ["quiz_id", "student_id", "is_submitted"]

    @action(detail=True, methods=["POST"], schema=QuizGradeSchema)
    async def grade(self, request, pk=None):
        submission = await self.get_object(pk)
        user = request.state.user

        if not (user.is_superuser or user.role in ["teacher", "admin"]):
            raise HTTPException(status_code=403, detail="Only teachers or admins can grade submissions.")

        data = await request.json()
        submission.score = data.get("score")
        submission.is_submitted = True
        await submission.save()

        return {"status": "success", "submission_id": str(submission.id), "score": submission.score}