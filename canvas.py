import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from progress import is_completed


load_dotenv()
TOKEN = os.getenv("CANVAS_TOKEN")


headers = {
    "Authorization": f"Bearer {TOKEN}"
}

params = {
    "bucket": "future"
}

url = "https://oslomet.instructure.com/api/v1/courses"

course_names = {
    34640: "DATS2300 - AlgDat",
    34622: "DAFE2200 - SysUt",
    34619: "ADSE2100 - MMI"
}

exams = [
    {
        "course": "DATS2300 - AlgDat",
        "type": "Eksamen",
        "date": datetime(2026, 11, 17, 9, 0, tzinfo=ZoneInfo("Europe/Oslo")),
        "duration": "3 timer"
    },
    {
        "course": "DAFE2200 - SysUt",
        "type": "Eksamen",
        "date": datetime(2026, 11, 25, 9, 0, tzinfo=ZoneInfo("Europe/Oslo")),
        "duration": "3 timer"
    },
    {
        "course": "ADSE2100 - MMI",
        "type": "Mappelevering",
        "date": datetime(2026, 11, 25, 11, 59, tzinfo=ZoneInfo("Europe/Oslo")),
        "duration": None
    }
]

def get_exams():
    return exams

def get_deadline(assignment):
    return assignment["deadline"]


def get_future_assignment_deadlines():
    now = datetime.now(timezone.utc)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        courses = response.json()
        all_assignments = []

        for course in courses:
            if course.get("id") in course_names:
                course_id = course.get("id")

                assignments_url = (
                    f"https://oslomet.instructure.com/api/v1/"
                    f"courses/{course_id}/assignments"
                )

                response_assignments = requests.get(
                    assignments_url,
                    headers=headers,
                    params=params
                )

                if response_assignments.status_code == 200:
                    assignments = response_assignments.json()

                    for assignment in assignments:
                        due_at = assignment.get("due_at")

                        if due_at is not None:
                            deadline = datetime.fromisoformat(
                                due_at.replace("Z", "+00:00")
                            )

                            time_left = deadline - now

                            all_assignments.append({
                                "assignment_id": assignment.get("id"),
                                "name": assignment.get("name"),
                                "deadline": deadline,
                                "time_left": time_left,
                                "course_id": course_id,
                                "course_name": course_names.get(course_id)
                            })

        all_assignments.sort(key=get_deadline)

        return all_assignments

    else:
        print("Noe gikk galt")
        print(response.status_code)
        print(response.text)

        return []

def format_deadlines(deadlines):
    message = ""

    for number, assignment in enumerate(deadlines, start=1):
        if is_completed(assignment["assignment_id"]):
            status = "✅"
        else:
            status = "⬜"

        days_left = assignment["time_left"].days
        local_deadline = assignment["deadline"].astimezone(
            ZoneInfo("Europe/Oslo")
        )

        formatted_deadline = local_deadline.strftime("%d.%m.%Y %H:%M")
        message += f"{status} {number}.\n{assignment['course_name']}\n{assignment['name']}\nFrist: {formatted_deadline}\n{days_left} dager igjen\n\n"

    return message


