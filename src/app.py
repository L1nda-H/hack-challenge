import json

from db import db
from flask import Flask, request
from db import Course
from db import User
from db import Assignment

import os

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here


# Get all courses
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    courses = Course.query.all()
    serialized_courses = [
        {"id": course.id, "code": course.code, "name": course.name}
        for course in courses
    ]
    return json.dumps({"courses": serialized_courses}), 200


# Create a course
@app.route("/api/courses/", methods=["POST"])
def create_course():
    data = request.get_json()
    code = data.get("code")
    name = data.get("name")

    if not code or not name:
        return json.dumps({"error": "Both code and name are required"}), 400

    course = Course(code=code, name=name)
    db.session.add(course)
    db.session.commit()

    return (
        json.dumps(
            {
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "assignments": [
                    {
                        "id": assignment.id,
                        "title": assignment.title,
                        "due_date": assignment.due_date,
                    }
                    for assignment in course.assignments
                ],
                "instructors": [
                    {
                        "id": instructor.id,
                        "name": instructor.name,
                        "netid": instructor.netid,
                    }
                    for instructor in course.instructors
                ],
                "students": [
                    {"id": student.id, "name": student.name, "netid": student.netid}
                    for student in course.students
                ],
            }
        ),
        201,
    )


# Get a specific course
@app.route("/api/courses/<int:id>/", methods=["GET"])
def get_course(id):
    course = Course.query.get(id)
    if course is None:
        return json.dumps({"error": "Course not found"}), 404

    serialized_course = {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "assignments": [
            {
                "id": assignment.id,
                "title": assignment.title,
                "due_date": assignment.due_date,
            }
            for assignment in course.assignments
        ],
        "instructors": [
            {"id": instructor.id, "name": instructor.name, "netid": instructor.netid}
            for instructor in course.instructors
        ],
        "students": [
            {"id": student.id, "name": student.name, "netid": student.netid}
            for student in course.students
        ],
    }

    return json.dumps(serialized_course), 200


# Delete a specific course
@app.route("/api/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get(id)
    if course is None:
        return json.dumps({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()

    serialized_course = {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "assignments": [
            {
                "id": assignment.id,
                "title": assignment.title,
                "due_date": assignment.due_date,
            }
            for assignment in course.assignments
        ],
        "instructors": [
            {"id": instructor.id, "name": instructor.name, "netid": instructor.netid}
            for instructor in course.instructors
        ],
        "students": [
            {"id": student.id, "name": student.name, "netid": student.netid}
            for student in course.students
        ],
    }
    return json.dumps(serialized_course), 200


# Create a user
@app.route("/api/users/", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    netid = data.get("netid")

    if not name or not netid:
        return json.dumps({"error": "Both name and netid are required"}), 400

    user = User(name=name, netid=netid)
    db.session.add(user)
    db.session.commit()

    return (
        json.dumps(
            {"id": user.id, "name": user.name, "netid": user.netid, "courses": []}
        ),
        201,
    )


# Get a specific user
@app.route("/api/users/<int:id>/", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404

    student_courses = [
        {"id": course.id, "code": course.code, "name": course.name}
        for course in user.courses_as_student
    ]

    # Get courses where the user is an instructor
    instructor_courses = [
        {"id": course.id, "code": course.code, "name": course.name}
        for course in user.courses_as_instructor
    ]

    # Combine both lists of courses
    courses = student_courses + instructor_courses
    serialized_user = {
        "id": user.id,
        "name": user.name,
        "netid": user.netid,
        "courses": courses,
    }

    return json.dumps(serialized_user), 200


# Add a user to a course
@app.route("/api/courses/<int:id>/add/", methods=["POST"])
def add_user_to_course(id):
    data = request.get_json()
    user_id = data.get("user_id")
    user_type = data.get("type")

    if not user_id or user_type not in ["student", "instructor"]:
        return (
            json.dumps(
                {"error": "Both user_id and type (student or instructor) are required"}
            ),
            400,
        )

    course = Course.query.get(id)
    user = User.query.get(user_id)

    if course is None or user is None:
        return json.dumps({"error": "Course or user not found"}), 404

    if user_type == "student":
        course.students.append(user)
    elif user_type == "instructor":
        course.instructors.append(user)

    db.session.commit()

    serialized_course = {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "assignments": [
            {
                "id": assignment.id,
                "title": assignment.title,
                "due_date": assignment.due_date,
            }
            for assignment in course.assignments
        ],
        "instructors": [
            {"id": instructor.id, "name": instructor.name, "netid": instructor.netid}
            for instructor in course.instructors
        ],
        "students": [
            {"id": student.id, "name": student.name, "netid": student.netid}
            for student in course.students
        ],
    }

    return json.dumps(serialized_course), 200


# Create an assignment for a course
@app.route("/api/courses/<int:id>/assignment/", methods=["POST"])
def create_assignment(id):
    data = request.get_json()
    title = data.get("title")
    due_date = data.get("due_date")

    if not title or not due_date:
        return json.dumps({"error": "Both title and due_date are required"}), 400

    course = Course.query.get(id)
    if course is None:
        return json.dumps({"error": "Course not found"}), 404

    assignment = Assignment(title=title, due_date=due_date, course_id=id)
    db.session.add(assignment)
    db.session.commit()

    serialized_assignment = {
        "id": assignment.id,
        "title": assignment.title,
        "due_date": assignment.due_date,
        "course": {
            "id": course.id,
            "code": course.code,
            "name": course.name,
        },
    }

    return json.dumps(serialized_assignment), 201


@app.route("/", methods=["GET"])
def greeting():
    return "hello"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
