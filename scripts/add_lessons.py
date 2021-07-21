import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
django.setup()

from django.contrib.auth.models import User
from activity.models import Lesson
from employee.models import Employee
from student.models import Student

def main():
    file_path = input('csv file location: ')
    # NOTE: Some students do not exist yet.
    # NOTE: Make saving safe: if class with this teacher and datetime exists: don't create another one

    return 0

if __name__ == '__main__':
    

    main()