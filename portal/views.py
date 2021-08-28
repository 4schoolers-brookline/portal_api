from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from parent.models import Parent
from manager.models import Manager
from employee.models import Employee
from student.models import Student

def index(request):
    context = {}
    if (request.user.is_authenticated):
        try:
            context['employee'] = Employee.objects.get(user = request.user)
            return redirect('employee_login')
        except:
            pass
        try:
            context['student'] = Student.objects.get(user = request.user)
            return redirect('student_login')
        except:
            pass
        try:
            context['parent'] = Parent.objects.get(user = request.user)
            return redirect('parent_login')
        except:
            pass
        try:
            context['manager'] = Manager.objects.get(user = request.user)
            return redirect('manager_login')
        except:
            pass


    return render(request, 'index.html')

def team(request):
    context = {}

    return render(request, 'team.jinja', context)



# Emailing password recovery <<<<<<<<<<

def forgot(request):
    context = {}

    if (request.method == 'POST'):
        data = request.POST.get('login')
        is_email = '@' in data

        if (is_email):
            try:
                acc = User.objects.get(email = data)
            except:
                context['invalid'] = True
                return render(request, 'emails/forgot_password.jinja', context)
        else:
            try:
                acc = User.objects.get(username = data)
            except:
                context['invalid'] = True
                return render(request, 'emails/forgot_password.jinja', context)

        
        mail_subject = '4Schoolers Pasword reset'
        message = render_to_string('emails/reset_email.jinja', {
            'user': acc,
            'uid':urlsafe_base64_encode(force_bytes(acc.pk)),
            'token':account_activation_token.make_token(acc),
        })
        to_email = acc.email

        
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return render(request, 'emails/email_sent.jinja', context)
        

    return render(request, 'emails/forgot_password.jinja', context)
def reset(request, uidb64, token):
     
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        context = {
            'user': user
        }
    except:
        context['error'] = True
        return render(request, 'emails/reseter.jinja', context)


    if (request.method == 'POST'):
        password = request.POST['password']
        pass_repeat = request.POST['password2']

        if (password != pass_repeat):
            context['invalid'] = True
            return render(request, 'emails/reseter.jinja', context)

        #check weak password
        if ( len(password) < 8 ):
            context['invalid'] = True
            return render(request, 'emails/reseter.jinja', context)

        try:
            user.set_password(password)
            user.save()
            return render(request, 'index.html', context)
        except:
            context['weak'] = True
            return render(request, 'emails/reseter.jinja', context)
            
    return render(request, 'emails/reseter.jinja', context)
