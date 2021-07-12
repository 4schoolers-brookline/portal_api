from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    
    path('login', views.login, name = 'parent_login'),
    
    path('profile', views.profile, name = 'parent_profile'),
    path('highlights', views.highlights, name = 'parent_highlights'),
]

