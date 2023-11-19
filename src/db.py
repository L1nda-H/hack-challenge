from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here


# Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    assignments = db.relationship("Assignment", backref="course", lazy=True)
    instructors = db.relationship(
        "User",
        secondary="course_instructor",
        back_populates="courses_as_instructor",
        lazy="dynamic",
    )
    students = db.relationship(
        "User",
        secondary="course_student",
        back_populates="courses_as_student",
        lazy="dynamic",
    )


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    netid = db.Column(db.String(20), unique=True, nullable=False)
    courses_as_instructor = db.relationship(
        "Course",
        secondary="course_instructor",
        back_populates="instructors",
        lazy="dynamic",
    )
    courses_as_student = db.relationship(
        "Course", secondary="course_student", back_populates="students", lazy="dynamic"
    )


# Many-to-Many association table for instructors
course_instructor = db.Table(
    "course_instructor",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

# Many-to-Many association table for students
course_student = db.Table(
    "course_student",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


# Assignment model
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
