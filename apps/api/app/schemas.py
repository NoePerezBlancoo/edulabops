from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    role: str = "student"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str

class CourseIn(BaseModel):
    name: str

class CourseOut(BaseModel):
    id: int
    name: str

class AssignmentIn(BaseModel):
    course_id: int
    title: str
    description: str = ""
    grader_image: str = "python:3.12-slim"

class AssignmentOut(BaseModel):
    id: int
    course_id: int
    title: str

class SubmissionIn(BaseModel):
    assignment_id: int
    repo_url: str

class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    status: str
    score: int
    feedback: str