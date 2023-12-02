from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# table
tutee_table = db.Table(
    "tutee association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)
tutor_table = db.Table(
    "tutor association",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)


# your classes here
class Post(db.Model):
    """
    Post Model
    """

    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    availability = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    course = db.Column(db.Integer, db.ForeignKey("course.id"))

    def __init__(self, **kwargs):
        """
        Initialize a Post object
        """
        self.title = kwargs.get("title", "")
        self.content = kwargs.get("content", "")
        self.availability = kwargs.get("availability", "")
        self.user = kwargs.get("user", "")
        self.course = kwargs.get("course", "")

    def serialize(self):
        """
        Serialize Post object
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "availability": self.availability,
            "user": self.user.simple_serialize(),
            "course": self.course.simple_serialize(),
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "availability": self.availability,
        }


class Course(db.Model):
    """
    Course Model
    """

    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    tutors = db.relationship(
        "User", secondary=tutor_table, back_populates="tutor_courses"
    )
    tutees = db.relationship(
        "User", secondary=tutee_table, back_populates="tutee_courses"
    )
    posts = db.relationship("Post", cascade="delete")

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
            "tutees": [u.simple_serialize() for u in self.tutees],
            "posts": [u.simple_serialize() for u in self.posts],
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
        "Course", secondary=tutor_table, back_populates="tutors"
    )
    tutee_courses = db.relationship(
        "Course", secondary=tutee_table, back_populates="tutees"
    )
    posts = db.relationship("Post", cascade="delete")

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
            "courses": [c.simple_serialize() for c in courses],
            "posts": [c.simple_serialize() for c in self.posts],
        }

    def simple_serialize(self):
        """ "
        Serialize User object without the courses field
        """
        return {"id": self.id, "name": self.name, "netid": self.netid}
