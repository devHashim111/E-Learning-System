from fastapi import APIRouter
from fapix.router import DefaultRouter
from fapix.core.router import register_urlpatterns
from .views import QuizViewSet, QuizSubmissionViewSet

router = APIRouter(prefix="/assessments", tags=["Assessments & Quizzes"])

assessment_router = DefaultRouter()
assessment_router.register("quizzes", QuizViewSet, basename="quiz")
assessment_router.register("submissions", QuizSubmissionViewSet, basename="submission")

urlpatterns = assessment_router.generate_urlpatterns()
register_urlpatterns(router, urlpatterns)