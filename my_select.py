from sqlalchemy import func, desc

from conf.db import session
from src.models import Student, Teacher, Group, Subject, Grade

DASHES = f'\n{"-" * 20}'


# -- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

def select_1(number_of_students=5):
    """
    Selects a specified number of students with the highest average grade from all subjects.

    Parameters:
        number_of_students (int): The number of students to select. Default is 5.

    Returns:
        None
    """
    query = session.query(Student.name, func.round(func.avg(Grade.grade), 1).label('avg_grade')) \
        .join(Grade, Grade.student_id == Student.id) \
        .group_by(Student.name) \
        .order_by(desc('avg_grade')) \
        .limit(number_of_students).all()

    print(f'\n{number_of_students} студентів із найбільшим\nсереднім балом з усіх предметів:{DASHES}')
    for student in query:
        print(f'{student.name}: {student.avg_grade} {DASHES}')


# -- Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    """
    Selects the student with the highest average grade for the specified subject.

    Parameters:
        subject_name (str): The name of the subject to select the student for.

    Returns:
        None
    """
    query = (session.query(Student.name, func.round(func.avg(Grade.grade), 1).label('avg_grade'))
               .join(Grade, Grade.student_id == Student.id)
               .join(Subject, Subject.id == Grade.subject_id)
               .filter(Subject.name == subject_name)
               .group_by(Student.name)
               .order_by(desc('avg_grade'))
               .first())

    if query:
        print(f'\nСтудент із найвищим середнім балом з предмету "{subject_name}":{DASHES}\n'
              f'{query.name} - {query.avg_grade} {DASHES}')
    else:
        print(f'\nСтудентів з предметом "{subject_name}" не знайдено.')


# -- Знайти середній бал у групах з певного предмета.

def select_3(subject_name):
    """
    Selects the average grade for the specified subject in all groups.

    Parameters:
        subject_name (str): The name of the subject to select the average grade for.

    Returns:
        None
    """
    query = (
        session.query(Group.name, func.round(func.avg(Grade.grade), 1).label('avg_grade'))
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .order_by(desc('avg_grade'))
        .all()
    )

    print(f'\nСередній бал у групах \nз предмета "{subject_name}":{DASHES}')
    for g in query:
        print(f'{g.name}, {g.avg_grade} {DASHES}')


# -- Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    """
    Selects the average grade on the entire table of grades.

    Parameters:
        None

    Returns:
        None
    """

    query = (session
           .query(func.round(func.avg(Grade.grade), 1).label('avg_grade'))
           .select_from(Grade)
           .all())

    print(f'\nСередній бал на потоці по всіх предметах: {query[0][0]}')


# -- Знайти які курси читає певний викладач.
def select_5(teacher_id):
    """
    Selects the courses that the specified teacher is teaching.

    Parameters:
        teacher_id (int): The ID of the teacher to select the courses for.

    Returns:
        None
    """
    query = (
        session.query(Teacher.name, Subject.name)
        .select_from(Subject)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .all()
    )

    if not query:
        print(f'\nВикладача з ID {teacher_id} не знайдено.')
        return

    print(f'\nКурси, які викладає {query[0][0]}:{DASHES}')
    for s in query:
        print(f'{s[1]} {DASHES}')


# -- Знайти список студентів у певній групі.
def select_6(group_name):
    query = (session.query(Student.name, Group.name)
                .select_from(Student).join(Group)
                .filter(Group.name == group_name).all())

    if not query:
        print(f'\nГрупи з назвою {group_name} не знайдено.')
        return

    print(f'\nСтуденти групи {group_name}:{DASHES}')
    for s in query:
        print(s[0])


# -- Знайти оцінки студентів у окремій групі з певного предмета.

def select_7(subject_name, group_name):
    """
    Selects the grades of students in a specific group for a specific subject.

    Parameters:
        subject_name (str): The name of the subject to select the grades for.
        group_name (str): The name of the group to select the grades for.

    Returns:
        None
    """
    query = (
        session.query(Student.name, Subject.name, Grade.grade)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )

    if not query:
        print(
            f'\nГрупи з назвою {group_name} або предмета {subject_name} не знайдено.'
        )
        return

    print(f'\nОцінки студентів у групі {group_name} з предмета {subject_name}:{DASHES}')
    for g in query:
        print(f'{g[0]} - {g[2]} {DASHES}')


# -- Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    """
    Selects the average grade that the specified teacher has for their subjects.

    Parameters:
        teacher_id (int): The ID of the teacher to select the average grade for.

    Returns:
        None
    """
    query = (
        session.query(Teacher.name, func.round(func.avg(Grade.grade), 1).label('avg_grade'))
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .group_by(Teacher.id)
        .filter(Teacher.id == teacher_id)
        .all()
    )

    if not query:
        print(f'\nВикладача з ID {teacher_id} не знайдено.')
        return

    print(f'Середній бал, який ставить\nвикладач {query[0][0]} - {query[0][1]}')


# -- Знайти список курсів, які відвідує студент.
def select_9(student_id):
    """
    Selects the courses that the specified student is enrolled in.

    Parameters:
        student_id (int): The ID of the student to select the courses for.

    Returns:
        None
    """
    query = (session.query(Student.name, Subject.name)
        .select_from(Student)
        .join(Grade)
        .join(Subject)
        .filter(Student.id == student_id)
        .distinct()
        .all())

    if not query:
        print(f'\nСтудента з ID {student_id} не знайдено.')
        return

    print(f'\nКурси, які відвідує \nстудент {query[0][0]}:{DASHES}')
    for s in query:
        print(s[1]+DASHES)


# -- Список курсів, які певному студенту читає певний викладач.

def select_10(student_id, teacher_id):
    """
    Selects the courses that the specified student reads by the specified teacher.

    Parameters:
        student_id (int): The ID of the student to select the courses for.
        teacher_id (int): The ID of the teacher to select the courses for.

    Returns:
        None
    """
    query = session.query(Student.name, Teacher.name, Subject.name).select_from(Student).distinct()
    query = query.join(Grade).join(Subject).join(Teacher).filter(Student.id == student_id, Teacher.id == teacher_id).all()

    if not query:
        print(f'\nСтудента з ID {student_id} або викладача з ID {teacher_id} не знайдено.')
        return

    print(f'\nКурси, які студенту {query[0][0]} \nчитає викладач {query[0][1]}:{DASHES}')
    for result in query:
        print(f'{result[2]}{DASHES}')


# select_1()
# select_2('Python core')
# select_3('Python core')
# select_4()
# select_5(6)
# select_6('Coders of the Galaxy')
# select_7('Python core', 'Coders of the Galaxy')
# select_8(6)
# select_9(32)
# select_10(4, 3)
