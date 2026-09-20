import pytest
from httpx import AsyncClient
from apps.courses.models import Course


def extract_data(res):
    if isinstance(res, dict) and "data" in res:
        return res["data"]
    return res


@pytest.mark.asyncio
async def test_course_crud_flow(
    client: AsyncClient,
    supervisor_auth: tuple[dict, dict],
):
    headers, supervisor = supervisor_auth

    course_payload = {
        "code": "CS101",
        "title": "Intro to Computer Science",
        "description": "Foundational programming course.",
        "instructor_id": str(supervisor["id"]),
        "is_published": True,
    }

    create_res = await client.post(
        "/courses/", json=course_payload, headers=headers
    )
    assert create_res.status_code in (200, 201), f"Course creation failed: {create_res.text}"

    # List Courses
    list_res = await client.get("/courses/", headers=headers)
    assert list_res.status_code == 200, f"List courses failed: {list_res.text}"


@pytest.mark.asyncio
async def test_enrollment_flow(
    client: AsyncClient,
    supervisor_auth: tuple[dict, dict],
    student_auth: tuple[dict, dict],
):
    sup_headers, supervisor = supervisor_auth
    std_headers, student = student_auth

    # 1. Create Course
    course_res = await client.post(
        "/courses/",
        json={
            "code": "MATH101",
            "title": "Calculus I",
            "instructor_id": str(supervisor["id"]),
        },
        headers=sup_headers,
    )
    assert course_res.status_code in (200, 201), f"Course creation failed: {course_res.text}"

    # 2. Extract course ID from database
    course_obj = await Course.filter(code="MATH101").first()
    assert course_obj is not None, "Could not find created course in database"
    course_id = str(course_obj.id)

    # 3. Enroll Student via EnrollmentViewSet endpoint (No trailing slash)
    enroll_res = await client.post(
        "/courses/enrollments",  # <--- Changed from "/courses/enrollments/"
        json={
            "course_id": course_id,
            "student_id": str(student["id"]),
        },
        headers=sup_headers,
    )
    assert enroll_res.status_code in (200, 201), f"Enrollment failed: {enroll_res.text}"