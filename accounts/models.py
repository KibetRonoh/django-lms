from django.db import models
from django.contrib.auth.models import AbstractUser


# Extending user Model to accommodate extra fields
class User(AbstractUser):
    occupation = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    is_instructor = models.BooleanField(default=False, null=True)
    user_image = models.ImageField(upload_to='media/users/', null=True, default='media/users/user.png', help_text='Dimension: 415 x 555')
    facebook_link = models.URLField(max_length=1000, null=True, blank=True)
    x_link = models.URLField(max_length=1000, null=True, blank=True)
    youtube_link = models.URLField(max_length=1000, null=True, blank=True)
    instagram_link = models.URLField(max_length=1000, null=True, blank=True)
    # about_author = models.TextField(null=True)


# social media model
class Socials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=1000, null=True, blank=True)
    x = models.URLField(max_length=1000, null=True, blank=True)
    youtube = models.URLField(max_length=1000, null=True, blank=True)
    instagram = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class InstructorApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.applicant)