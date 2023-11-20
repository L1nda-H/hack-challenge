from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# table
tutee_table = db.Table(
    "tutee association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)
tutor_table = db.Table(
    "tutor association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

# your classes here


class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    tutors = db.relationship(
        "User", secondary=tutor_table, back_populates="tutor_courses")
    tutees = db.relationship(
        "User", secondary=tutee_table, back_populates="tutee_courses")

    def __init__(self, **kwargs):
        """
        Initialize a Course object
        """
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize Course object
        """
        return {
            "id": self.id,
            "name": self.name,
            "tutors": [u.simple_serialize() for u in self.tutors],
            "tutees": [u.simple_serialize() for u in self.tutees]
        }

    def simple_serialize(self):
        """
        Simple Serialize Course object
        """
        return {
            "id": self.id,
            "name": self.name,
        }

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    tutor_courses = db.relationship(
        "Course", secondary=tutor_table, back_populates="instructors")
    tutee_courses = db.relationship(
        "Course", secondary=tutee_table, back_populates="students")

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")
        self.type = kwargs.get("type", "")

    def serialize(self):
        """
        Serialize User object, returning all courses involved with
        """

        courses = []
        for i in self.tutor_courses:
            courses.append(i)
        for j in self.tutee_courses:
            courses.append(j)
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in courses]
        }

    def simple_serialize(self):
        """"
        Serialize User object without the courses field
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }