from faker import Faker
from conf.db import session
from src.models import Student, Teacher, Group, Subject, Grade

faker = Faker('uk-UA')

NUMBER_OF_SUBJECTS = 8
NUMBER_OF_TEACHERS = 5
NUMBER_OF_GROUPS = 3
NUMBER_OF_STUDENTS = 50
NUMBER_OF_GRADES_FOR_STUDENT = 20
SUBJECTS = (
    "Python core",
    "Soft skills",
    "Python Web",
    "English",
    "HTML+CSS",
    "JavaScript",
    "Python date science",
    "Career skills",
)


def seed_groups(session=session):
    groups = ("DRY_KISS.py", "Coders of the Galaxy", "Gruppe Sechs")
    for name in groups:
        group = Group(name=name)
        session.add(group)
        session.commit()


# seed_groups()

def seed_teachers(session=session):
    for _ in range(NUMBER_OF_TEACHERS):
        teacher = Teacher(name=faker.name())
        session.add(teacher)
        session.commit()


def seed_subjects(session=session):
    for subject in SUBJECTS:
        subject = Subject(name=subject, teacher_id=faker.random.randint(1, NUMBER_OF_TEACHERS))
        session.add(subject)
        session.commit()


def seed_students(session=session):
    for _ in range(NUMBER_OF_STUDENTS):
        student = Student(name=faker.name(), group_id=faker.random.randint(1, NUMBER_OF_GROUPS))
        session.add(student)
        session.commit()


def seed_grades(session=session):
    for student_id in range(1, NUMBER_OF_STUDENTS + 1):
        for _ in range(NUMBER_OF_GRADES_FOR_STUDENT):
            grade = Grade(
                student_id=student_id,
                subject_id=faker.random.randint(1, NUMBER_OF_SUBJECTS),
                grade=faker.random.randint(2, 12),
                grade_date=faker.date_this_year(),
            )
            session.add(grade)
        session.commit()


seed_grades()
