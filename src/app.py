from db import db
from flask import Flask, request
import json
from db import Course, User, Post

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/")
def base():
    """
    Base endpoint
    """
    return success_response("Welcome to LearnWell", 200)

# Courses
@app.route("/api/courses/")
def get_courses():
    """
    Gets all courses
    """
    courses = [c.serialize() for c in Course.query.all()]
    return success_response({"courses": courses}, 200)


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Creates a course

    name: course's title
    """
    body = json.loads(request.data)
    course_name = body.get("name")
    if course_name is None:
        return failure_response("Sufficient information not provided", 400)
    new_course = Course(name=course_name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

# User
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Creates a user

    name: user's name
    netid: user's netid
    """
    body = json.loads(request.data)
    user_name = body.get("name")
    user_netid = body.get("netid")
    if user_name is None or user_netid is None:
        return failure_response("Sufficient information not provided", 400)
    new_user = User(name=user_name, netid=user_netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a user from database, and removes them as tutors/tutees

    user_id: id of user to delete
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


# Relational Method
@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Adds user to a course as a tutor or tutee

    user_id: user id
    type: type of user, tutor or tutee
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    user_type = body.get("type")
    if user_id is None or user_type is None:
        return failure_response("Sufficient information not provided", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    user.type = user_type
    if user_type == "tutee":
        course.tutees.append(user)
    else:
        course.tutors.append(user)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/posts/")
def get_posts(user_id):
    """
    Make a post by a user
    """
    posts = [p.serialize() for p in Post.query.all()]
    return success_response({"posts": posts}, 200)

@app.route("/api/posts/<int:user_id>/", methods=["POST"])
def create_post(user_id):
    """
    Make a post by a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body = json.loads(request.data)
    title = body.get("title")
    content = body.get("content")
    availability = body.get("availability")
    course = body.get("course")
    new_post = Post(title=title, content=content, availability=availability)
    db.session.add(new_post)
    db.session.commit()
    return success_response(course.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
