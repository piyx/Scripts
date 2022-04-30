'''
GRADE POINT SCALE

| Score Range        | Grade Points |
| ------------------ | ------------ |
| 90 <= marks <= 100 | 10           |
| 80 <= marks < 90   | 9            |
| 70 <= marks < 80   | 8            |
| 60 <= marks < 70   | 7            |
| 45 <= marks < 60   | 6            |
| 40 <= marks < 45   | 4            |
| 0 <= marks < 40    | 0            |

SGPA = Σ(Course credits * Grade Points) / Σ(Course Credits)

NOTE: This script works only for CSE/ISE Physics cycle.
Change the 'semestersubjects.json' to modify the subjects/
'''

import json
from dataclasses import dataclass

with open('semester_subjects.json', 'r') as f:
    semesters = json.load(f)["semesters"]


@dataclass
class Subject:
    name: str
    credit: int
    gradepoint: int


def SGPA(subjects: list[Subject]) -> float:
    gradepoints = sum(sub.gradepoint * sub.credit for sub in subjects)
    totalcredits = sum(sub.credit for sub in subjects)
    return gradepoints/totalcredits


allsubjects = []

for i, semester in enumerate(semesters, 1):
    print(f"Enter gradepoint for semester {i}")
    subjects = []
    for subjectname, credit in semester.items():
        gradepoint = int(input(f"{subjectname}: "))
        subjects.append(Subject(
            name=subjectname,
            credit=credit,
            gradepoint=gradepoint
        ))

    allsubjects.extend(subjects)
    print(f"\nSGPA for SEMESTER {i} is: {SGPA(subjects):.2f}\n")

print(f"\nOverall CGPA is: {SGPA(allsubjects)}")