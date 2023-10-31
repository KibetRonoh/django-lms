from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('refund', views.refund, name='refund'),
    path('privacy', views.privacy, name='privacy'),
    path('contact', views.contact, name='contact'),
    path('instructor', views.instructor, name='instructor'),
]
