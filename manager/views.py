from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student, Exam
from django.contrib.auth.models import User
from activity.models import Lesson, Submission
from manager.models import Manager, Request
from parent.models import Parent
from bank.models import StudentAccount, StudentLessonBill
import re
import json
import datetime
from datetime import timedelta
from django.utils import timezone
import pytz

def validation_manager(func):
     def validation(request, *args, **kwargs):
         try:
             manager = Manager.objects.get(user = request.user)
             return func(request, *args, **kwargs)
         except Exception as e:
             context = {'error': e}
             auth.logout(request)
             return render(request, 'manager/404.jinja', context)
     return validation

def index(request):
    return 'Hello manager'

def login(request):
    context = {}
    if (request.user.is_authenticated):
        return redirect('manager_profile')

    if (request.method == 'POST'):
        if '@' in request.POST['login']:
            email = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email = email)
            except:
                context['invalid'] = True
                return render(request, 'manager/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('manager_profile')
            else:
                context['invalid'] = True
                return render(request, 'manager/login.jinja', context)
        else:
            username = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username = username)
            except:
                context['invalid'] = True
                return render(request, 'manager/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('manager_profile')
            else:
                context['invalid'] = True
                return render(request, 'manager/login.jinja', context)

    return render(request, 'manager/login.jinja', context)

@login_required
@validation_manager
def password(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'manager/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'manager/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('employee_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'manager/password.jinja', context)

    return render(request, 'manager/password.jinja', context)

@login_required
@validation_manager
def logout(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    auth.logout(request)
    return redirect('manager_login')

@login_required
@validation_manager
def profile(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    manager = Manager.objects.get(user = request.user)

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            employee.image = avatar
            employee.save()
        else:
            employee.school = request.POST.get('school')
            graduation_year = int(request.POST.get('graduation_year'))
            employee.bio = request.POST.get('bio')
            employee.languages = request.POST.get('languages')
            employee.interests = request.POST.get('interests')
            employee.address = request.POST.get('address')
            employee.city = request.POST.get('city')
            employee.state = request.POST.get('state')
            employee.zip_code = request.POST.get('zip_code')
            employee.save()
        return redirect('employee_profile')



    return render(request, 'manager/profile.jinja', context)
    return redirect('')

@login_required
@validation_manager
def employee_list(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: x.priority or 1)
    return render(request, 'manager/employee_list.jinja', context)

@login_required
@validation_manager
def students_list(request):
    context = {}
    context['manager'] = manager = Manager.objects.get(user = request.user)
    context['students'] = students = manager.students.all() # sorted(list(Employee.objects.all()), key = lambda x: x.priority)
    context['active_students'] = students.filter(is_active = True)
    context['inactive_students'] = students.filter(is_active = False)
    return render(request, 'manager/students_list.jinja', context)

@login_required
@validation_manager
def parents_list(request):
    context = {}
    context['manager'] = manager = Manager.objects.get(user = request.user)
    students = manager.students.all()
    context['parents'] = [p for p in Parent.objects.all() if p.child in students]
    return render(request, 'manager/parents_list.jinja', context)

@login_required
@validation_manager
def req(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']
        owner = request.user
        user_request = Request(owner = owner, description = req)
        user_request.save()
    return render(request, 'manager/request.jinja', context)

@login_required
@validation_manager
def req_list(request):
    context = {}
    return redirect('')

@login_required
@validation_manager
def lessons(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    return render(request, 'manager/lessons.jinja', context)

@login_required
@validation_manager
def lessons_list(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    lessons = []
    for employee in context['manager'].employees.all():
        lessons += Lesson.objects.filter(teacher = employee)
    for student in context['manager'].students.all():
        lessons += [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    lessons = set(lessons)
    context['lessons'] = sorted(list(lessons), key = lambda x: x.start.timestamp(), reverse = True)

    return render(request, 'manager/lessons_list.jinja', context)

@login_required
@validation_manager
def lesson(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    l = Lesson.objects.get(id = id)
    if l.teacher in context['manager'].employees.all() or any(i in l.students.all() for i in context['manager'].students.all()):
        pass
    else:
        return render(request, 'manager/404.jinja')
    context['lesson'] = l
    context['students_registered'] = l.students.all()
    context['homeworks'] = l.homework_submissions.all()

    return render(request, 'manager/lesson.jinja', context)

@login_required
@validation_manager
def lesson_delete(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)
    if lesson.teacher in context['manager'].employees.all() or any(i in lesson.students.all() for i in context['manager'].students.all()):
        pass
    else:
        return render(request, 'manager/404.jinja')

    if (request.method == 'POST'):
        if timezone.now() > lesson.start or lesson.start - timezone.now() < timedelta(days=1):
            return render(request, 'manager/403.jinja', context)
        lesson.delete()
        return redirect('manager_lessons')

    return render(request, 'manager/lesson_delete.jinja', context)

@login_required
@validation_manager
def lesson_edit(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)

    if lesson.teacher in context['manager'].employees.all() or any(i in lesson.students.all() for i in context['manager'].students.all()):
        pass
    else:
        return render(request, 'manager/404.jinja')

    context['students'] = sorted(list(context['manager'].students.all()), key = lambda x: x.user.get_full_name())
    context['employees'] = Employee.objects.all()

    context['start_time'] = lesson.start - datetime.timedelta(hours = 4)
    context['end_time'] = lesson.end - datetime.timedelta(hours = 4)

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        students = request.POST.getlist('student')
        teacher = request.POST['teacher']
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            ss = [Student.objects.get(pk=id) for id in students]
        except:
            context['error'] = 'One of the students does not exist'
            return render(request, 'manager/lesson_edit.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
            if end_parsed < start_parsed:
                context['error'] = 'There was a problem with the selected time'
                return render(request, 'manager/lesson_edit.jinja', context)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'manager/lesson_edit.jinja', context)

        lesson.name = name
        lesson.description = description
        for student in lesson.students.all():
            if (student not in ss):
                lesson.students.remove(student)
        lesson.students.add(*ss)
        lesson.subject = subject
        lesson.start = start_parsed
        lesson.end = end_parsed

        lesson.save()
        return redirect('manager_lessons')

    return render(request, 'manager/lesson_edit.jinja', context)

@login_required
@validation_manager
def lesson_add(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['students'] = sorted(list(context['manager'].students.all()), key = lambda x: x.user.get_full_name())
    context['employees'] = Employee.objects.all()

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        students = request.POST.getlist('student')
        teacher = request.POST['teacher']
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            ss = [Student.objects.get(pk=id) for id in students]
        except:
            context['error'] = 'One of the students does not exist'
            return render(request, 'manager/lesson_add.jinja', context)

        try:
            t = Employee.objects.get(pk = teacher)
        except:
            context['error'] = 'Teacher does not exist'
            return render(request, 'manager/lesson_add.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
            if end_parsed < start_parsed:
                context['error'] = 'There was a problem with the selected time <'
                return render(request, 'manager/lesson_add.jinja', context)
        except:
            context['error'] = 'There was a problem with the selected time except'
            return render(request, 'manager/lesson_add.jinja', context)

        lesson = Lesson(name = name, description = description, teacher = t, start = start_parsed, end = end_parsed)

        lesson.subject = subject
        lesson.save()
        lesson.students.add(*ss)

        lesson.save()

    return render(request, 'manager/lesson_add.jinja', context)

@login_required
@validation_manager
def highlights_student(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['student'] = Student.objects.get(id = id)
    context['student_id'] = context['student'].id
    context['lessons'] = lessons = [lesson for lesson in Lesson.objects.all() if (context['student'] in lesson.students.all())]
    context['classes'] = len(lessons)

    try:
        studentacc = StudentAccount.objects.get(student = Student.objects.get(id = id))
    except:
        studentacc = StudentAccount(student = Student.objects.get(id = id))
        studentacc.save()

    context['balance'] = studentacc.get_units_left()



    hrs = 0
    for lesson in lessons:
        diff = lesson.end-lesson.start
        hrs += diff.total_seconds()/3600
    context['hours'] = round(hrs, 2)

    return render(request, 'manager/highlights_student.jinja', context)

@login_required
@validation_manager
def highlights_employee(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['employee'] = Employee.objects.get(id = id)
    context['employee_id'] = context['employee'].id
    context['lessons'] = lessons = Lesson.objects.filter(teacher = context['employee'])
    context['classes'] = len(lessons)

    students = set()
    ctr = 0
    for lesson in lessons:
        ctr += (lesson.end-lesson.start).total_seconds()/3600
        for student in lesson.students.all():
            students.add(student)

    context['students'] = len(students)
    context['hours'] = ctr


    return render(request, 'manager/highlights_employee.jinja', context)

@login_required
@validation_manager
def student_add(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    if request.method == 'POST':

        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        bio = request.POST['bio']
        is_male = (request.POST['gender'] == "male")
        languages = request.POST['languages']
        interests = request.POST['interests']
        school = request.POST['school']
        graduation = request.POST['graduation_year']
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['zip']
        state = request.POST['state']
        country = request.POST['country']

        user = User(
            first_name = fname,
            last_name = lname,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()

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
        try:
            student.graduation_year = int(graduation)
        except:
            pass
        student.save()

        context['manager'].students.add(student)
        context['manager'].save()
        return redirect('manager_student_list')
    return render(request, 'manager/student_add.jinja', context)

@login_required
@validation_manager
def employee_add(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        bio = request.POST['bio']
        is_male = (request.POST['gender'] == "male")
        languages = request.POST['languages']
        interests = request.POST['interests']
        school = request.POST['school']
        graduation = request.POST['graduation_year']
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['zip']
        state = request.POST['state']
        country = request.POST['country']
        title = request.POST['title']
        education = request.POST['education']
        subjects = request.POST['subjects']
        level = 3
        is_fulltime = (request.POST['education'] == "yes")
        priority = 1
        user, created = User.objects.get_or_create(
            first_name = fname,
            last_name = lname,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()

        employee, created = Employee.objects.get_or_create(
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
            is_active = True,
            title = title,
            education = education,
            level = level,
            subjects = subjects,
            is_fulltime = is_fulltime,
            priority = int(priority)
        )
        try:
            employee.graduation_year = int(graduation)
        except:
            pass
        employee.save()

        context['manager'].employees.add(employee)
        context['manager'].save()
        return redirect('manager_employee_list')
    return render(request, 'manager/employee_add.jinja', context)

@login_required
@validation_manager
def parent_add(request):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['students'] = context['manager'].students.all()
    if request.method == 'POST':

        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        id = request.POST['student']
        try:
            student = Student.objects.get(pk=id)
        except:
            context['error'] = 'Student does not exist'
            return render(request, 'manager/parent_add.jinja', context)

        user, created = User.objects.get_or_create(
            first_name = fname,
            last_name = lname,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()

        parent, created = Parent.objects.get_or_create(
            user = user,
            phone = phone,
            child = student
        )
        parent.save()

        return redirect('manager_parent_list')
    return render(request, 'manager/parent_add.jinja', context)

@login_required
@validation_manager
def student(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['student'] = student = Student.objects.get(pk = id)

    context['languages'] = student.get_languages()
    context['interests'] = student.get_interests()

    if student not in context['manager'].students.all():
        return render(request, 'manager/404.jinja')

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            student.image = avatar
            student.save()
        else:
            student.school = request.POST.get('school')
            student.graduation_year = int(request.POST.get('graduation_year'))
            student.bio = request.POST.get('bio')
            student.languages = request.POST.get('languages')
            student.interests = request.POST.get('interests')
            student.address = request.POST.get('address')
            student.city = request.POST.get('city')
            student.state = request.POST.get('state')
            student.zip_code = request.POST.get('zip_code')
            password = request.POST.get('password')
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, password)
            if not mat:
                context['error'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
                return render(request, 'manager/student.jinja', context)
            student.user.set_password(password)
            student.user.save()
            student.save()
        return redirect('manager_student', id)



    return render(request, 'manager/student.jinja', context)

@login_required
@validation_manager
def employee(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['employee'] = employee = Employee.objects.get(pk = id)

    context['languages'] = employee.get_languages()
    context['interests'] = employee.get_interests()
    context['subjects'] = employee.get_subjects()

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            employee.image = avatar
            employee.save()
        else:
            employee.school = request.POST.get('school')
            employee.graduation_year = int(request.POST.get('graduation_year'))
            employee.bio = request.POST.get('bio')
            employee.languages = request.POST.get('languages')
            employee.interests = request.POST.get('interests')
            employee.address = request.POST.get('address')
            employee.city = request.POST.get('city')
            employee.state = request.POST.get('state')
            employee.zip_code = request.POST.get('zip_code')
            employee.save()
        return redirect('manager_employee', id)



    return render(request, 'manager/employee.jinja', context)

@login_required
@validation_manager
def parent(request, id):
    context = {}
    context['manager'] = Manager.objects.get(user = request.user)
    context['parent'] = parent = Parent.objects.get(pk = id)
    student = parent.child

    if student not in context['manager'].students.all():
        return render(request, 'manager/404.jinja')

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            parent.image = avatar
            parent.save()
        else:
            parent.phone = request.POST['phone']
            parent.save()
        return redirect('manager_parent', id)

    return render(request, 'manager/parent.jinja', context)

def to_datetime(s):
    date = s.split(' ')[0].split('/')
    time = s.split(' ')[1].split(':')
    x = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

    return x
