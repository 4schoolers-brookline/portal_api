import sys
sys_path = input("System path to project")
sys.path.append(sys_path)
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
django.setup()
import csv


from django.contrib.auth.models import User
from activity.models import Lesson
from employee.models import Employee
from student.models import Student
import datetime


def add_lesson(line):
    print(line)
    subject = line[1]
    students_list = line[2].split(',')
    students = []
    for fname in students_list:
        try:
            user = User.objects.get(first_name = fname)
            student = Student.objects.get(user = user)
            students.append(student)
        except:
            print('Student {} does not exist'.format(fname))

    date = line[0].split('/')
    time_begin = line[3].split(':')
    time_end = line[4].split(':')
    print(date,time_begin, time_end)

    begin = datetime.datetime(2021, int(date[0]), int(date[1]), int(time_begin[0]), int(time_begin[1]) )
    end = datetime.datetime(2021, int(date[0]), int(date[1]), int(time_end[0]), int(time_end[1]) )
    teacher_fname = line[5]
    try:
        user = User.objects.get(first_name = teacher_fname)
        teacher = Employee.objects.get(user = user)
    except:
        print('Teacher: {} does not exist'.format(teacher_fname))

    lesson = Lesson(name = 'Regular {} class'.format(subject), teacher = teacher, subject = subject, start = begin, end = end)
    lesson.save()
    for student in students:
        lesson.students.add(student)
    
    lesson.save()

def file_add(path):
     
    with open(path) as f:
        reader = csv.reader(f, delimiter = '\t')
        header = next(reader)
        for row in reader:
            add_lesson(row)
        

def main():
    x = input('File(1) or CLI(2): ')
    if (x=='1'):
        path = input("File path: ")
        file_add(path)
    elif (x=='2'):
        delimeter = '\t'
        x = input('Insert line: ').split(delimeter)
        add_lesson(x)
if __name__ == '__main__':
    main()
