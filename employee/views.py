from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student, Exam
from django.contrib.auth.models import User
from activity.models import Lesson, Submission
from manager.models import Request
from bank.models import StudentAccount, StudentLessonBill
import re
import datetime
from datetime import timedelta
from django.utils import timezone
import pytz

def validation_employee(func):

     def validation(request, *args, **kwargs):
         try:
             employee = Employee.objects.get(user = request.user)
             return func(request, *args, **kwargs)
         except Exception as e:
             auth.logout(request)
             context = {'error': e}
             return render(request, 'employee/404.jinja', context = context)
     return validation

def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['employee'] = Employee.objects.get(user = request.user)
        return redirect('employee_highlights')
    else:
        return redirect('employee_login')

def login(request):
    context = {}
    if (request.user.is_authenticated):
        return redirect('employee_profile')

    if (request.method == 'POST'):
        if '@' in request.POST['login']:
            email = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email = email)
            except:
                context['invalid'] = True
                return render(request, 'employee/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('employee_profile')
            else:
                context['invalid'] = True
                return render(request, 'employee/login.jinja', context)
        else:
            username = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username = username)
            except:
                context['invalid'] = True
                return render(request, 'employee/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('employee_profile')
            else:
                context['invalid'] = True
                return render(request, 'employee/login.jinja', context)

    return render(request, 'employee/login.jinja', context)

@login_required
@validation_employee
def logout(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    auth.logout(request)
    return redirect('employee_login')

@login_required
@validation_employee
def profile(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    employee = Employee.objects.get(user = request.user)

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



    return render(request, 'employee/profile.jinja', context)

@login_required
@validation_employee
def password(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'employee/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'employee/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('employee_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'employee/password.jinja', context)

    return render(request, 'employee/password.jinja', context)

@login_required
@validation_employee
def student(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['student'] = Student.objects.get(id = id)
    context['interests'] = (context['student'].get_interests() or 'Education')
    context['languages'] = (context['student'].get_languages() or 'English')

    return render(request, 'employee/student.jinja', context)

@login_required
@validation_employee
def student_add(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
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
            student.graduation_year = graduation
        except:
            pass
        student.save()
        return redirect('employee_directory')
    return render(request, 'employee/student_add.jinja', context)

@login_required
@validation_employee
def directory(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['students'] = Student.objects.all() # sorted(list(Employee.objects.all()), key = lambda x: x.priority)
    context['active_students'] = Student.objects.filter(is_active = True)
    context['inactive_students'] = Student.objects.filter(is_active = False)
    return render(request, 'employee/directory.jinja', context)

@login_required
@validation_employee
def req(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']
        owner = request.user
        user_request = Request(owner = owner, description = req)
        user_request.save()

    return render(request, 'employee/request.jinja', context)

@login_required
@validation_employee
def highlights(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
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


    return render(request, 'employee/highlights.jinja', context)

@login_required
@validation_employee
def lessons(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    return render(request, 'employee/lessons.jinja', context)

@login_required
@validation_employee
def lessons_list(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = context['employee'])
    context['lessons'] = sorted(list(lessons), key = lambda x: x.start.timestamp(), reverse = True)

    return render(request, 'employee/lessons_list.jinja', context)

@login_required
@validation_employee
def lesson(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    l = Lesson.objects.get(id = id)
    if context['employee'] != l.teacher:
        return render(request, 'employee/404.jinja')
    context['lesson'] = l
    context['students_registered'] = l.students.all()
    context['homeworks'] = l.homework_submissions.all()

    try:
        submission = l.homework_submissions.all().get(owner = request.user)
    except:
        submission = None

    context['submission'] = submission

    context['homework_file'] = context['classwork_file'] = context['submission_file'] = False
    try:
        context['homework_file'] = l.homework.file
    except:
        pass
    try:
        context['classwork_file'] = l.classwork.file
    except:
        pass
    try:
        context['submission_file'] = submission.file
    except:
        pass

    if (request.method == 'POST'):
        description = request.POST['descr']
        try:
            uploaded_file = request.FILES['subm']

            subm = Submission(name = 'lesson{}'.format(l.pk), description = description, owner = request.user, type = 'Homework_Submission', file = uploaded_file, account_type = 'student')
        except:
            subm = Submission(name = 'lesson{}'.format(l.pk), description = description, owner = request.user, type = 'Homework_Submission', account_type = 'student')
        subm.save()

        l.homework_submissions.add(subm)
        l.save()
        return redirect('employee_lesson', l.id)

    return render(request, 'employee/lesson.jinja', context)

@login_required
@validation_employee
def lesson_edit(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)
    if context['employee'] != lesson.teacher:
        return render(request, 'employee/404.jinja')
    context['students'] = sorted(list(Student.objects.all()), key = lambda x: x.user.get_full_name())

    context['start_time'] = lesson.start - datetime.timedelta(hours = 4)
    context['end_time'] = lesson.end - datetime.timedelta(hours = 4)

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        students = request.POST.getlist('student')
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            ss = [Student.objects.get(pk=id) for id in students]
        except:
            context['error'] = 'One of the students does not exist'
            return render(request, 'employee/lesson_edit.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
            if end_parsed < start_parsed:
                context['error'] = 'There was a problem with the selected time'
                return render(request, 'employee/lesson_edit.jinja', context)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'employee/lesson_edit.jinja', context)

        lesson.name = name
        lesson.description = description
        for student in lesson.students.all():
            if (student not in ss):
                lesson.students.remove(student)
        lesson.students.add(*ss)
        lesson.subject = subject
        lesson.start = start_parsed
        lesson.end = end_parsed


        # Classwork
        try:
            cw = lesson.classswork
            cw_exists = True
        except:
            cw_exists = False

        try:
            cw_name = request.POST['cw_name']
            cw_descr = request.POST['cw_descr']
            cw_file = request.FILES['cw_file']
            cw_file_exists = True


        except:
            cw_file_exists = False

        if (cw_name or cw_descr or cw_file_exists):
            if (cw_exists):
                cw.name = cw_name
                if (cw_file_exists):
                    cw.file = cw_file
                cw.description = cw_descr
                cw.save()
            else:
                cw = Submission(name = cw_name, description = cw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Classwork')

                if (cw_file_exists):
                    cw.file = cw_file
                cw.save()
                lesson.classwork = cw

        # Homework
        try:
            hw = lesson.homework
            hw_exists = True
        except:
            hw_exists = False

        try:
            hw_name = request.POST['hw_name']
            hw_descr = request.POST['hw_descr']
            hw_file = request.FILES['hw_file']
            hw_file_exists = True


        except:
            hw_file_exists = False

        if (hw_name or hw_descr or hw_file_exists):
            try:
                hw.name = hw_name or ''
                if (hw_file_exists):
                    hw.file = hw_file
                hw.description = hw_descr or ''
                hw.save()
            except:
                hw = Submission(name = hw_name, description = hw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Homework')
                if (hw_file_exists):
                    hw.file = hw_file
                hw.save()
                lesson.homework = hw



        lesson.save()
        return redirect('employee_lessons')

    return render(request, 'employee/lesson_edit.jinja', context)

@login_required
@validation_employee
def lesson_add(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['students'] = sorted(list(Student.objects.all()), key = lambda x: x.user.get_full_name())

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        students = request.POST.getlist('student')
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            ss = [Student.objects.get(pk=id) for id in students]
        except:
            context['error'] = 'One of the students does not exist'
            return render(request, 'employee/lesson_add.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
            if end_parsed < start_parsed:
                context['error'] = 'There was a problem with the selected time'
                return render(request, 'employee/lesson_add.jinja', context)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'employee/lesson_add.jinja', context)

        lesson = Lesson(name = name, description = description, teacher = context['employee'], start = start_parsed, end = end_parsed)

        lesson.subject = subject
        lesson.save()
        lesson.students.add(*ss)

        lesson.save()
        # Classwork
        try:
            cw = lesson.classswork
            cw_exists = True
        except:
            cw_exists = False

        try:
            cw_name = request.POST['cw_name']
            cw_descr = request.POST['cw_descr']
            cw_file = request.FILES['cw_file']
            cw_file_exists = True


        except:
            cw_file_exists = False

        if (cw_name or cw_descr or cw_file_exists):
            if (cw_exists and cw):
                cw.name = cw_name
                if (cw_file_exists):
                    cw.file = cw_file
                cw.description = cw_descr
                cw.save()
            else:
                cw = Submission(name = cw_name, description = cw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Classwork')

                if (cw_file_exists):
                    cw.file = cw_file
                cw.save()
                lesson.classwork = cw

        # Homework
        try:
            hw = lesson.homework
            hw_exists = True
        except:
            hw_exists = False

        try:
            hw_name = request.POST['hw_name']
            hw_descr = request.POST['hw_descr']
            hw_file = request.FILES['hw_file']
            hw_file_exists = True


        except:
            hw_file_exists = False

        if (hw_name or hw_descr or hw_file_exists):
            if (hw_exists and  hw):

                hw.name = hw_name
                if (hw_file_exists):
                    hw.file = hw_file
                hw.description = hw_descr
                hw.save()
            else:
                hw = Submission(name = hw_name, description = hw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Homework')
                if (hw_file_exists):
                    hw.file = hw_file
                hw.save()
                lesson.homework = hw

        lesson.save()

        return redirect('employee_lessons')

    return render(request, 'employee/lesson_add.jinja', context)

@login_required
@validation_employee
def lesson_delete(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)
    if context['employee'] != lesson.teacher:
        return render(request, 'employee/404.jinja')

    if (request.method == 'POST'):
        
        lesson.delete()
        return redirect('employee_lessons')

    return render(request, 'employee/lesson_delete.jinja', context)

@login_required
@validation_employee
def lesson_clone(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    l = context['lesson'] = Lesson.objects.get(pk = id)
    if context['employee'] != l.teacher:
        return render(request, 'employee/404.jinja')
    context['students'] = sorted(list(Student.objects.all()), key = lambda x: x.user.get_full_name())

    context['start_time'] = l.start - datetime.timedelta(hours = 4)
    context['end_time'] = l.end - datetime.timedelta(hours = 4)

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        students = request.POST.getlist('student')
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            ss = [Student.objects.get(pk=id) for id in students]
        except:
            context['error'] = 'One of the students does not exist'
            return render(request, 'employee/lesson_edit.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
            if end_parsed < start_parsed:
                context['error'] = 'There was a problem with the selected time'
                return render(request, 'employee/lesson_edit.jinja', context)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'employee/lesson_edit.jinja', context)


        lesson = Lesson(name = name, description = description, subject = subject , teacher = context['employee'], start = start_parsed, end = end_parsed)



        # Classwork
        try:
            cw = lesson.classswork
            cw_exists = True
        except:
            cw_exists = False

        try:
            cw_name = request.POST['cw_name']
            cw_descr = request.POST['cw_descr']
            cw_file = request.FILES['cw_file']
            cw_file_exists = True


        except:
            cw_file_exists = False

        if (cw_name or cw_descr or cw_file_exists):
            if (cw_exists):
                cw.name = cw_name
                if (cw_file_exists):
                    cw.file = cw_file
                cw.description = cw_descr
                cw.save()
            else:
                cw = Submission(name = cw_name, description = cw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Classwork')

                if (cw_file_exists):
                    cw.file = cw_file
                cw.save()
                lesson.classwork = cw

        # Homework
        try:
            hw = lesson.homework
            hw_exists = True
        except:
            hw_exists = False

        try:
            hw_name = request.POST['hw_name']
            hw_descr = request.POST['hw_descr']
            hw_file = request.FILES['hw_file']
            hw_file_exists = True


        except:
            hw_file_exists = False

        if (hw_name or hw_descr or hw_file_exists):
            try:
                hw.name = hw_name or ''
                if (hw_file_exists):
                    hw.file = hw_file
                hw.description = hw_descr or ''
                hw.save()
            except:
                hw = Submission(name = hw_name, description = hw_descr, owner = context['employee'].user, account_type = 'employee', type = 'Homework')
                if (hw_file_exists):
                    hw.file = hw_file
                hw.save()
                lesson.homework = hw



        lesson.save()
        lesson.students.add(*ss)
        return redirect('employee_lessons')

    return render(request, 'employee/lesson_clone.jinja', context)



def to_datetime(s):
    date = s.split(' ')[0].split('/')
    time = s.split(' ')[1].split(':')
    x = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

    return x
