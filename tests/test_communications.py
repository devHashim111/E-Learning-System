import pytest
from httpx import AsyncClient
from apps.courses.models import Course  # Adjust import based on your app structure


def extract_data(res):
    if isinstance(res, dict) and "data" in res:
        return res["data"]
    return res


@pytest.mark.asyncio
async def test_chatroom_and_message_operations(
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
            "code": "ENG101",
            "title": "English Literature",
            "instructor_id": str(supervisor["id"]),
        },
        headers=sup_headers,
    )
    assert course_res.status_code in (200, 201), f"Course creation failed: {course_res.text}"

    # 2. Retrieve Course ID from DB or via GET /courses/
    course_obj = await Course.filter(code="ENG101").first()
    if course_obj:
        course_id = str(course_obj.id)
    else:
        # Fallback via GET endpoint if model isn't imported directly
        list_res = await client.get("/courses/", headers=sup_headers)
        assert list_res.status_code == 200, f"Course listing failed: {list_res.text}"
        courses = extract_data(list_res.json())
        if isinstance(courses, dict) and "items" in courses:
            courses = courses["items"]
        
        target = next((c for c in courses if c.get("code") == "ENG101"), None)
        assert target and "id" in target, f"Could not locate created course in list: {courses}"
        course_id = str(target["id"])

    # 3. Create Chat Room
    room_res = await client.post(
        "/communications/rooms",
        json={
            "course_id": course_id,
            "name": "General Discussion",
        },
        headers=sup_headers,
    )
    assert room_res.status_code in (200, 201), f"Room creation failed: {room_res.text}"