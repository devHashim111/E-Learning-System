from fastapi import APIRouter
from fapix.router import DefaultRouter
from fapix.core.router import register_urlpatterns
from .views import CourseViewSet, EnrollmentViewSet

router = APIRouter(prefix="/courses", tags=["Courses & Enrollments"])

course_router = DefaultRouter()
course_router.register("", CourseViewSet, basename="course")
course_router.register("enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = course_router.generate_urlpatterns()
register_urlpatterns(router, urlpatterns)