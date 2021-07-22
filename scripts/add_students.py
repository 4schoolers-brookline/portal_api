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

def main():
    path = input("File path: ")
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            user, created = User.objects.get_or_create(
                first_name=row[0],
                last_name=row[1],
                username=row[2],
                email=row[4],
                password=row[3]
                )
            if created:
                student, created = Student.objects.get_or_create(
                    user = user,
                    phone = row[5],
                    bio = row[6],
                    languages = row[8],
                    interests = row[9],
                    school = row[10],
                    address = row[12],
                    city = row[13],
                    zip_code = row[14],
                    state = row[15],
                    country = row[16],
                )
                if created:
                    try:
                        student.graduation_year=row[11]
                        student.save()
                    except:
                        student.graduation_year= None
                    student.is_male = (row[7] == "yes" )
                    student.save()
    return 0

if __name__ == '__main__':
    main()
