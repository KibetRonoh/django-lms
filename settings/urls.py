from django.urls import path
from . import views


urlpatterns = [
    path('site-setting', views.site_setting, name='site-setting'),
]