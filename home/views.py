from django.shortcuts import render
from core.models import Category, Course, UserCourse, Video
from settings.models import SiteSetting
from .models import Contact, Testimonial, Faq, Term, Privacy, Refund
from accounts.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# this is a home view to handle all the index page functions
def index(request):
    testimonials = Testimonial.objects.filter(featured=True)
    settings = SiteSetting.objects.all()
    courses = Course.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    featured_course = Course.objects.filter(status='FEATURED').order_by('?')[0:3]
    popular = Course.objects.filter(status='POPULAR').order_by('?')[0:3]
    enrollments = UserCourse.objects.all().count()
    resources = Video.objects.all().count()

    catid = request.GET.get('category')
    if catid:
        courses = Course.objects.filter(category=catid)
    else:
        courses = Course.objects.all()
    context = {
        'settings': settings,
        'courses': courses,
        'categories': categories,
        'popular': popular,
        'featured_course': featured_course,
        'testimonials': testimonials,
        'enrollments': enrollments,
        'resources': resources,
    }
    return render(request, 'home/index.html', context)


def contact(request):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

    context = {
        'settings': settings,
        'categories': categories,
    }

    return render(request, 'home/contact.html', context)


def faq(request):
    categories = Category.objects.all().order_by('id')[0:6]
    settings = SiteSetting.objects.all()
    faqs = Faq.objects.all()

    context = {
        'settings': settings,
        'faqs': faqs,
        'categories': categories,
    }
    return render(request, 'home/faq.html', context)


def terms(request):
    categories = Category.objects.all().order_by('id')[0:6]
    settings = SiteSetting.objects.all()
    terms = Term.objects.all()

    context = {
        'settings': settings,
        'terms': terms,
        'categories': categories,
    }
    return render(request, 'home/terms.html', context)


def privacy(request):
    settings = SiteSetting.objects.all()
    privacy = Privacy.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]

    context = {
        'settings': settings,
        'privacy': privacy,
        'categories': categories,
    }
    return render(request, 'home/privacy.html', context)


def refund(request):
    settings = SiteSetting.objects.all()
    refunds = Refund.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]

    context = {
        'settings': settings,
        'refunds': refunds,
        'categories': categories,
    }
    return render(request, 'home/refund.html', context)


def instructor(request):
    categories = Category.objects.all().order_by('id')[0:6]
    settings = SiteSetting.objects.all()
    instructor = User.objects.filter(is_instructor=True)
    paginator = Paginator(instructor, 8)
    page = request.GET.get('page')
    instructors = paginator.get_page(page)

    context = {
        'settings': settings,
        'instructors': instructors,
        'categories': categories,
    }
    return render(request, 'home/instructor.html', context)