import sys
sys_path = input("System path to project")
sys.path.append(sys_path)
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
django.setup()
import csv
import datetime

from django.contrib.auth.models import User
from activity.models import Lesson
from employee.models import Employee
from student.models import Student

#Doesnt work
def main():
    path = input("File path: ")
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            date = row[0].split('/')
            time_start = row[3].split(':')
            time_end = row[4].split(':')
            teacher = Employee.objects.get(user__first_name = row[5])
            students_name = row[2].split('&')
            students_list = []
            for name in students_name:
                students = Student.objects.filter(user__first_name = name)
                students = list(students)
                students_list += students
            subject = row[1]
            time_start = datetime.datetime(2021, int(date[0]), int(date[1]), int(time_start[0]), int(time_start[1]))
            time_end = datetime.datetime(2021, int(date[0]), int(date[1]), int(time_end[0]), int(time_end[1]))
            #lesson, created = Lesson.objects.get_or_create(name = "Unnamed lesson", teacher = teacher, subject = subject, start = time_start, end = time_end)
            #for student in students_list:
                #lesson.students.add(student)
    return 0

if __name__ == '__main__':
    main()
