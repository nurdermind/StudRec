import os

import pandas as pd
from fastapi import FastAPI

from schemas import StudentRequest, StudentResponse
from studrec import StudRec

app = FastAPI()

STUDREC_VEC_NBRS_PATH = 'studrec.dump.pickle'
DATASET_PATH = 'student_data.csv'
N_NEIGHBORS = 5
ALGORITHM = 'brute'


def get_studrec() -> StudRec:
    df = pd.read_csv(DATASET_PATH)
    df.set_index('student_id', inplace=True)

    studrec = StudRec(
        dataset=df,
        n_neighbors=N_NEIGHBORS,
        algorithm=ALGORITHM
    )
    if os.path.exists(STUDREC_VEC_NBRS_PATH):
        studrec.load_vec_nbrs_from_file(STUDREC_VEC_NBRS_PATH)
    else:
        studrec.fit()

    return studrec


studrec = get_studrec()


@app.post("/find", response_model=list[StudentResponse])
async def find(student: StudentRequest):
    students = studrec.find([student.dict()])[0]
    return [StudentResponse(**s) for s in students]


@app.post("/find_indexes", response_model=list[int])
async def find(student: StudentRequest):
    students_ids = studrec.find_indexes([student.dict()])[0]
    return students_ids
