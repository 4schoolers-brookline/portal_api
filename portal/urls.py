"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views, searchbar

urlpatterns = [
    path('', views.index),
    path('reset/<uidb64>/<token>/',views.reset, name='reset'),
    path('admin/', admin.site.urls),
    path('forgot', views.forgot, name = 'forgot'),
    path('api/student_searchbar', searchbar.student_searchbar, name = 'student_searchbar'),
    path('api/employee_searchbar', searchbar.employee_searchbar, name = 'employee_searchbar'),
    path('api/manager_searchbar', searchbar.manager_searchbar, name = 'manager_searchbar'),
    path('student/', include('student.urls')),
    path('corporation/', include('corporation.urls')),
    path('manager/', include('manager.urls')),
    path('parent/', include('parent.urls')),
    path('employee/', include('employee.urls')),
    path('activity/', include('activity.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
