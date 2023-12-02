Expected Functionality

Welcome screen
GET /
<HTTP STATUS CODE 200>
{
    "message": "Welcome to LearnWell"
}

Get all courses
GET /api/courses/
<HTTP STATUS CODE 200>
{
    "courses": [
        {
            "id": <ID>,
            "name": <Course Name>,
            "tutors":[<ALL TUTORS SERIALIZED WITHOUT COURSE>],
            "tutees":[<ALL TUTEES SERIALIZED WITHOUT COURSE>],
            "posts":[<ALL POSTS SERIALIZED WITHOUT COURSE>]
        },
        // ... other courses
    ]
}

Create a course
POST /api/courses/
{
    "name": "Intro to Backend Development"
}
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "name": "Intro to Backend Development",
    "tutors":[],
    "tutees":[],
    "posts":[]
}

Create a user
POST /api/users/
{
    "name": "John Doe",
    "netid": "jd123"
}
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "name": "John Doe",
    "netid": "jd123",
    "courses":[],
    "posts":[]
}

Delete a user
DELETE /api/users/<int:user_id>/
<HTTP STATUS CODE 200>
{
    "id": <user_id>,
    "name": <User Name>,
    "netid": <User NetID>,
    "courses":[<ALL COURSES SERIALIZED WITHOUT USER>],
    "posts":[<ALL POSTS SERIALIZED WITHOUT USER>]
}

Add user to course
POST /api/courses/<int:course_id>/add/
{
    "user_id": <User ID>,
    "type": "tutor" // or "tutee"
}
<HTTP STATUS CODE 200>
{
    "id": <course_id>,
    "name": <Course Name>,
    "tutors":[<ALL TUTORS SERIALIZED WITHOUT COURSE>],
    "tutees":[<ALL TUTEES SERIALIZED WITHOUT COURSE>],
    "posts":[<ALL POSTS SERIALIZED WITHOUT COURSE>]
}

Get all posts by a user
GET /api/posts/
<HTTP STATUS CODE 200>
{
    "posts": [
        {
            "id": <ID>,
            "title": <Post Title>,
            "content": <Post Content>
            "availability":<Post availability>,
            "user":<User>,
            "course":<Course>
        },
        // ... other posts
    ]
}

Make a post by a user
POST /api/posts/<int:user_id>/
{
    "title": "Need Help in OCaml",
    "content": "Struggling with OCaml",
    "availability": "Weekends",
    "course": "CS 3110"
}
<HTTP STATUS CODE 201>
{
    "id": <ID>,
    "title": "Need Help in OCaml",
    "content": "Struggling with OCaml",
    "availability": "Weekends",
    "user":<User details>,
    "course": "CS 3110"
}
