from django.contrib.auth.views import LogoutView
from django.urls import path

from PySchool import settings
from . import views

# this are the routes for accounts apps
urlpatterns = [
    path('register', views.register, name='register'),
    # path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    # path('password_reset/done/', views.password_reset_done, name='password_reset_done'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('socials', views.user_socials, name='socials'),
    path('become-instructor', views.become_instructor, name='become-instructor'),
    path('student-details', views.student_details, name='student-details'),
]