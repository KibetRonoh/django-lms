from django.db import models
from django.contrib.auth import get_user_model
from tinymce import models as tinymce_models

User = get_user_model()

class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.CharField(max_length=20)
    contact_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + self.subject


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = tinymce_models.HTMLField(max_length=200)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Faq(models.Model):
    BELONGS = (
        ('SITE', 'SITE'),
        ('OTHER', 'OTHER')
    )
    title =models.CharField(max_length=50)
    belongs = models.CharField(choices=BELONGS, max_length=1000)
    description = tinymce_models.HTMLField()

    def __str__(self):
        return self.title


class Term(models.Model):
    heading = models.CharField(max_length=200)
    body = tinymce_models.HTMLField(max_length=10000)

    def __str__(self):
        return self.heading


class Privacy(models.Model):
    heading = models.CharField(max_length=200)
    body = tinymce_models.HTMLField(max_length=10000)

    def __str__(self):
        return self.heading


class Refund(models.Model):
    heading = models.CharField(max_length=200)
    body = tinymce_models.HTMLField(max_length=10000)

    def __str__(self):
        return self.heading
