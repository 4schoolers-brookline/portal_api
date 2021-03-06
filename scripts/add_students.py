import sys
sys_path = input("System path to project: ")
sys.path.append(sys_path)
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
django.setup()
import csv

from django.contrib.auth.models import User
from activity.models import Lesson
from employee.models import Employee
from student.models import Student

def add_student():
    data = input('First Name,Last Name,username,password,Email,Phone,bio,is_male,languages,interests,school,graduation year,address,city,zip,state,country').split(',')

    # Data
    fname = data[0]
    lname = data[1]
    username = data[2]
    password = data[3]
    email = data[4]
    phone = data[5]
    bio = data[6]
    is_male = (data[7]=='yes')
    languages = data[8]
    interests = data[9]
    school = data[10]
    graduation = data[11]
    address = data[12]
    city = data[13]
    zip_code = data[14]
    state = data[15]
    country = data[16]

    #user creation
    user = User(
        first_name = fname,
        last_name = lname,
        username = username,
        email = email
    )
    user.set_password(password)
    user.save()

    # student creation
    student = Student(
        user = user,
        phone = phone,
        bio = bio,
        is_male = is_male,
        languages = languages,
        interests = interests,
        school = school,
        address = address,
        city = city,
        zip_code = zip_code,
        state = state,
        country = country,
        is_active = True
    )
    student.save()
    return 0

def read_file():
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
                user.set_password(row[3])
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


def main():
    x = input('File(1) or CLI(2)')
    if (x=='1'):
        read_file()
    elif (x=='2'):
        add_student()


if __name__ == '__main__':
    main()
