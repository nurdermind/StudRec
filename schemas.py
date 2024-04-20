from pydantic import BaseModel


class StudentRequest(BaseModel):
    faculty: str
    cathedra: str
    rank: int
    scienceStars: int
    sportStars: int
    creationStars: int
    volunteerStars: int


class StudentResponse(StudentRequest):
    student_id: int

