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
                email=row[3]
                )
            user.set_password(row[4])
            user.save()
            if created:
                employee, created = Employee.objects.get_or_create(
                    user = user,
                    title = row[6],
                    education = row[7],
                    languages = row[9],
                    interests = row[10],
                    subjects = row[11],
                    phone = row[14],
                    bio = row[15],
                    school = row[16],
                    address = row[18],
                    city = row[19],
                    zip_code = row[20],
                    state = row[21],
                    country = row[22],
                    level = row[23]
                )
                if created:
                    try:
                        employee.birth_date=row[12]
                        employee.save()
                    except:
                        employee.birth_date= None
                    try:
                        employee.graduation_year=row[17]
                        employee.save()
                    except:
                        employee.graduation_year= None
                    try:
                        employee.priority = row[8]
                        employee.save()
                    except:
                        employee.priority = None
                    employee.is_male = (row[12] == "yes" )
                    employee.is_fulltime = (row[5] == "yes")
                    employee.save()
    return 0

if __name__ == '__main__':
    main()
