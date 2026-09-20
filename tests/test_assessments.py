import pytest
from httpx import AsyncClient
from apps.courses.models import Course
def extract_data(res):
    if isinstance(res, dict) and "data" in res:
        return res["data"]
    return res

@pytest.mark.asyncio
async def test_quiz_and_submission_lifecycle(
    client: AsyncClient,
    supervisor_auth: tuple[dict, dict],
    student_auth: tuple[dict, dict],
):
    sup_headers, supervisor = supervisor_auth
    std_headers, student = student_auth

    # Setup Course
    course_res = await client.post(
    "/courses/",
    json={
        "code": "PHY101",
        "title": "Physics I",
        "instructor_id": str(supervisor["id"]),
    },
    headers=sup_headers,
)

    assert course_res.status_code in (200, 201), course_res.text

    c_json = course_res.json()

    course = await Course.get(code="PHY101")
    course_id = str(course.id)


    # Create Quiz
    quiz_res = await client.post(
        "/assessments/quizzes",
        json={
            "title": "Midterm Exam",
            "total_marks": 100,
            "due_date": "2026-12-31T23:59:59Z",
            "course_id": course_id,
            "course": course_id,  # Handles schema setups expecting 'course' foreign key
        },
        headers=sup_headers,
    )
    # assert quiz_res.status_code in (200, 201)
    assert quiz_res.status_code in (200, 201), quiz_res.text
@pytest.mark.asyncio
async def test_quiz_invalid_course_id_returns_400_or_422(
    client: AsyncClient,
    supervisor_auth: tuple[dict, dict],
):
    sup_headers, _ = supervisor_auth
    
    quiz_res = await client.post(
        "/assessments/quizzes",
        json={
            "title": "Invalid Quiz",
            "total_marks": 100,
            "due_date": "2026-12-31T23:59:59Z",
            "course_id": "invalid-uuid",
        },
        headers=sup_headers,
    )
    
    # ✅ CORRECT: Expect validation rejection for malformed UUID
    assert quiz_res.status_code in (400, 422), f"Expected 400 or 422, got {quiz_res.status_code}: {quiz_res.text}"