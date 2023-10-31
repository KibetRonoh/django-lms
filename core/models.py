from django.db import models
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from tinymce import models as tinymce_models
User = get_user_model()


# this function validates image dimensions
def validate_image(image):
    max_height = 1920
    max_width = 1080
    height = image.file.height
    width = image.file.width
    if width > max_width or height > max_height:
        raise ValidationError("Height or Width is larger than what is allowed")


class Category(models.Model):
    icon = models.CharField(max_length=200, null=True, blank=True, help_text='example: fa-brands fa-angular')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def get_all_categories(self):
        return Category.objects.all().order_by('-id')


class Author(models.Model):
    author_profile = models.ImageField(upload_to='media/authors')
    name = models.ForeignKey(User, models.CASCADE, null=True)
    about_author = models.TextField()
    facebook_link = models.URLField(max_length=1023, null=True)
    x_link = models.URLField(max_length=1023, null=True)
    instagram_link = models.URLField(max_length=1023, null=True)
    youtube_link = models.URLField(max_length=1023, null=True)

    def __str__(self):
        return str(self.name)


class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (
        ('PUBLISHED', 'NORMAL'),
        ('DRAFT', 'DRAFT'),
        ('LATEST', 'lATEST'),
        ('FEATURED', 'FEATURED'),
        ('POPULAR', 'POPULAR'),
    )
    CERTIFICATES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    FEATURED_AS = (
        ('0', 'NORMAL'),
        ('3', 'NEW'),
        ('2', 'HOT'),
        ('1', 'BESTSELLER')
    )
    title = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = tinymce_models.HTMLField()
    featured_image = models.ImageField(upload_to='media/featured_image', null=True, help_text='Recommended Dimensions: 1000 x 600')
    featured_video = models.CharField(max_length=300, null=True, help_text='eg: https://www.youtube.com/watch?v=6stlCkUDG_s&list=PL4Gr5tOAPttLOY9IrWVjJlv4CtkYI5cI_')
    price = models.FloatField(max_length=6, default=0)
    discount = models.IntegerField(null=True, default=0, blank=0, help_text='discount is %, put 0 if it has no discount')
    discounted_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    certificate = models.CharField(choices=CERTIFICATES, max_length=100, null=True)
    slug = models.SlugField(default='', max_length=400, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    featured_as = models.CharField(choices=FEATURED_AS, max_length=100, null=True)

    def __str__(self):
        return self.title

    # calculating average review
    def average_review(self):
        reviews = Review.objects.filter(course=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg

    def count_review(self):
        reviews = Review.objects.filter(course=self).aggregate(count=Count('course_id'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = int(reviews['count'])
        return cnt

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

    def get_checkout_url(self):
        from django.urls import reverse
        return reverse("checkout", kwargs={'slug': self.slug})

    def get_paypal_checkout_url(self):
        from django.urls import reverse
        return reverse("paypal-checkout", kwargs={'slug': self.slug})

    def get_stripe_checkout_url(self):
        from django.urls import reverse
        return reverse("stripe-page", kwargs={'slug': self.slug})

    def get_stripe_success_url(self):
        from django.urls import reverse
        return reverse("stripe-success", kwargs={'slug': self.slug})

    def get_watch_url(self):
        from django.urls import reverse
        return reverse("course-take", kwargs={'slug': self.slug})

    def get_review_url(self):
        from django.urls import reverse
        return reverse("review", kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Course)


class WhatToLearn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Requirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='media/video_thumbnail', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_video_id = models.CharField(max_length=100, null=True, blank=True, help_text='Eg: 9iKZ_uojvxw')
    time_duration = models.FloatField(null=True, default=0)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    has_completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title


# class Payment(models.Model):
#     order_id = models.CharField(max_length=100, null=True, blank=True)
#     payment_id = models.CharField(max_length=100, null=True, blank=True)
#     user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.first_name + " - " + self.course.title


class Subscription(models.Model):
    VALIDITY = (
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('Lifetime', 'Lifetime')
    )
    plan = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2)
    popular = models.BooleanField(default=False)
    validity = models.CharField(choices=VALIDITY, max_length=100, null=True)

    def get_subscription_url(self):
        from django.urls import reverse
        return reverse("confirm-subscription", kwargs={'id': self.id})

    def __str__(self):
        return self.plan


class Features(models.Model):
    package = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    feature = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Features"

    def __str__(self):
        return self.package.plan


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    subscription = models.ForeignKey(Subscription, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscription.plan


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = tinymce_models.HTMLField(max_length=500, null=True)
    rating = models.IntegerField(default=0, null=True)
    rating_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title
