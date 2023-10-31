from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from settings.models import SiteSetting
from .models import Category, Level, Course, Video, UserCourse, Subscription, Order, Review, Author, Section
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import json
import stripe
from django.conf import settings

# Getting your stripe api details
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


# this is a view to read categories
def read_cat(request, id):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories to be displayed on this specific page
    categories = Category.objects.all().order_by('id')[0:6]
    # getting categories by id
    cats = Category.objects.get(id=id)
    # filtering categories by above results
    courses = Course.objects.filter(category=cats)

    context = {
        'settings': settings,
        'cats': cats,
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'core/read_cat.html', context)


# this is the courses view, it has all the functions related to causes
def courses(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting all courses
    courses = Course.objects.all().order_by('?')
    # this is the function to get pages and courses per page
    paginator = Paginator(courses, 6)
    page = request.GET.get('page')
    paged_courses = paginator.get_page(page)
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    # getting course level
    levels = Level.objects.all()
    # filtering courses based on status
    featured = Course.objects.filter(status='FEATURED')
    popular = Course.objects.filter(status='POPULAR')
    latest = Course.objects.filter(status='LATEST')
    # filtering and counting based on status
    featured_count = Course.objects.filter(status='FEATURED').count()
    popular_count = Course.objects.filter(status='POPULAR').count()
    latest_count = Course.objects.filter(status='LATEST').count()
    course_count = Course.objects.all().count()
    free_course_count = Course.objects.filter(price=0).count()
    paid_course_count = Course.objects.filter(price__gte=1).count()

    context = {
        'categories': categories,
        'levels': levels,
        'courses': paged_courses,
        'course_count': course_count,
        'latest_count': latest_count,
        'popular_count': popular_count,
        'featured_count': featured_count,
        'free_course_count': free_course_count,
        'paid_course_count': paid_course_count,
        'featured': featured,
        'popular': popular,
        'latest': latest,
        'settings': settings,
    }
    return render(request, 'core/courses.html', context)


def filter_data(request):
    settings = SiteSetting.objects.all()
    category = request.GET.getlist('category[]')

    if category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    context = {
        'settings': settings,
        'course': course,
    }
    t = render_to_string('ajax/course.html', context)

    return JsonResponse({'data': t})

# this is the view function to excecute course searching
def search(request):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    query = request.GET['query']
    courses = Course.objects.filter(title__icontains=query)

    context = {
        'settings': settings,
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'core/search.html', context)


# this is the function that handles specific course details
@login_required
def course_details(request, slug):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    # filtering course by slug
    course = Course.objects.filter(slug=slug)
    popular = Course.objects.filter(status='POPULAR').order_by('?')[0:2]
    # course_author = Course.objects.filter(author='author').order_by('-id')[0:2]

    # fav_course = get_object_or_404(Course, slug=slug)
    # is_favorite = False
    # if fav_course.favorite.filter(id=request.user.id).exists():
    #     is_favorite = True

    # just a message to be displayed in template
    money_back = '30-Day Money-Back Guarantee'
    course_review = Course.objects.get(slug=slug)

    # filtering reviews by course
    reviews = Review.objects.filter(course=course_review)

    reviews2 = Review.objects.filter(course_id=course_review)

    # counting reviews based on star rating given
    five_review_count = Review.objects.filter(course_id=course_review, rating=5).count()
    four_review_count = Review.objects.filter(course_id=course_review, rating=4).count()
    three_review_count = Review.objects.filter(course_id=course_review, rating=3).count()
    two_review_count = Review.objects.filter(course_id=course_review, rating=2).count()
    one_review_count = Review.objects.filter(course_id=course_review, rating=1).count()
    total_review_count = Review.objects.filter(course_id=course_review).count()

    # calculating total time for the course
    time_duration = Video.objects.filter(course__slug=slug).aggregate(
        sum=Sum('time_duration'))  # aggregate returns a dict
    time_duration = int(time_duration.get('sum'))  # getting value of a dict

    sections = Section.objects.filter(course__slug=slug)

    course_id = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'course': course,
        'popular': popular,
        'sections': sections,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'categories': categories,
        'reviews': reviews,
        'reviews2': reviews2,
        'total_review_count': total_review_count,
        'five_review_count': five_review_count,
        'four_review_count': four_review_count,
        'three_review_count': three_review_count,
        'two_review_count': two_review_count,
        'one_review_count': one_review_count,
        'money_back': money_back,
        'settings': settings,
        # 'course_author': course_author,
        # 'overall_review': overall_review,
        # 'five_review_percentage': five_review_percentage,
    }
    return render(request, 'core/course_details.html', context)


def page_not_found(request):
    settings = SiteSetting.objects.all()
    context = {
        'settings': settings,
    }
    return render(request, 'core/404.html', context)


# checkout function to handle checkout page
def checkout(request, slug):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    course = Course.objects.get(slug=slug)

    # checking if course is free
    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'You have successfully enrolled')
        return redirect('my-courses')
    else:
        course = Course.objects.get(slug=slug)

    context = {
        'course': course,
        'categories': categories,
        'settings': settings,
    }
    return render(request, 'core/checkout.html', context)


# function to handle paypal checkout
def paypal_checkout(request, slug):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    course = Course.objects.get(slug=slug)

    # if course is free then enroll without invoking payment process
    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'You have successfully enrolled')
        return redirect('my-courses')
    else:
        course = Course.objects.get(slug=slug)

    context = {
        'course': course,
        'categories': categories,
        'settings': settings,
    }
    return render(request, 'core/paypal-checkout.html', context)


# if course is a paid one then this function will excecute that process
def payment_complete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    course = Course.objects.get(slug=body['courseId'])
    UserCourse.objects.create(
        user=request.user,
        course=course,
    )
    return redirect('my-courses')


# this is the function that handles user specific enrolled courses
@login_required
def my_courses(request):
    settings = SiteSetting.objects.all()
    my_courses = UserCourse.objects.filter(user=request.user)
    completed_courses = UserCourse.objects.filter(user=request.user, has_completed=True)
    active_courses = UserCourse.objects.filter(user=request.user, has_completed=False)
    categories = Category.objects.all().order_by('id')[0:6]
    my_course_count = UserCourse.objects.filter(user=request.user).count()

    context = {
        'my_courses': my_courses,
        'completed_courses': completed_courses,
        'active_courses': active_courses,
        'categories': categories,
        'my_course_count': my_course_count,
        'settings': settings,
    }
    return render(request, 'core/my-courses.html', context)


# this function is responsible for handling course resources and how the are displayed to user
@login_required
def course_take(request, slug):
    settings = SiteSetting.objects.all()
    course = Course.objects.filter(slug=slug)
    lecture = request.GET.get('lecture')
    # video = Video.objects.filter(id=lecture).first()
    video = Video.objects.get(id=lecture) if Video.objects.filter(id=lecture).exists() else None

    course_id = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    review_id = Course.objects.get(slug=slug)
    try:
        check_review = Review.objects.get(user=request.user, course=review_id)
    except Review.DoesNotExist:
        check_review = None

    context = {
        'course': course,
        'video': video,
        'check_enroll': check_enroll,
        'check_review': check_review,
        'settings': settings,
    }
    return render(request, 'core/course-take.html', context)


def subscription(request):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    subscriptions = Subscription.objects.all().order_by('id')

    context = {
        'subscriptions': subscriptions,
        'categories': categories,
        'settings': settings,
    }
    return render(request, 'core/subscription.html', context)


def confirm_subscription(request, id):
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]
    subscription = Subscription.objects.get(id=id)
    context = {
        'subscription': subscription,
        'categories': categories,
        'settings': settings,
    }
    return render(request, 'core/confirm-subscription.html', context)


def subscription_complete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    subscription = Subscription.objects.get(id=body['subscriptionId'])
    Order.objects.create(
        user=request.user,
        subscription=subscription,
    )
    return JsonResponse('Payment completed!', safe=False)


def payment_successful(request):
    return render(request, 'core/payment-successful.html')


def review(request, slug):
    course = Course.objects.get(slug=slug)
    context = {
        'course': course,
    }
    return render(request, 'core/review.html', context)


def submit_review(request, slug):
    if request.method == 'GET':
        course = Course.objects.get(slug=slug)
        comment = request.GET.get('comment')
        rating = request.GET.get('rating')
        user = request.user

        if Review.objects.filter(user=user).exists():
            messages.error(request, 'You have already submitted a Review for this course')
            return redirect('course_details', slug)
        Review.objects.create(
            user=user, course=course, comment=comment, rating=rating
        )

    course_id = Course.objects.get(slug=slug)
    try:
        check_review = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_review = None

    context = {
        'course': course,
        'check_review': check_review,
    }
    return redirect('course_details', slug)


def favorite(request, slug):
    fav_course = get_object_or_404(Course, slug=slug)
    if fav_course.favorite.filter(id=request.user.id).exists():
        fav_course.favorite.remove(request.user)
    else:
        fav_course.favorite.add(request.user)
    return HttpResponseRedirect(fav_course.get_absolute_url())


@login_required
def my_reviews(request):
    settings = SiteSetting.objects.all()
    reviews = Review.objects.filter(user=request.user)
    categories = Category.objects.all().order_by('id')[0:6]
    my_course_count = UserCourse.objects.filter(user=request.user).count()

    context = {
        'reviews': reviews,
        'categories': categories,
        'my_course_count': my_course_count,
        'settings': settings,
    }
    return render(request, 'core/my-reviews.html', context)


class CreateCheckoutSessionView(generic.View):
    def post(self, *arg, **kwargs):
        host = self.request.get_host()

        course_id = self.request.POST.get('course')
        course = Course.objects.get(slug=course_id)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int((course.price * (100 - course.discount) * 100) / 100),
                        'product_data': {
                            'name': course.title,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://{}{}'.format(host, reverse('stripe-payment-success')),
            cancel_url='http://{}{}'.format(host, reverse('stripe-payment-cancelled')),
        )
        intent = UserCourse(user=self.request.user, course=course)
        intent.save()
        return redirect(checkout_session.url, code=303)


def stripe_page(request, slug):
    course = Course.objects.get(slug=slug)

    context = {
        'course': course,
    }
    return render(request, 'core/stripe-page.html', context)


def stripe_success(request, slug):
    course = Course.objects.get(slug=slug)

    context = {
        'course': course,
    }
    return render(request, 'core/stripe-success.html', context)


def stripe_payment_success(request):
    settings= SiteSetting.objects.all()
    context = {
        'payment_status': 'success',
        'settings': settings,
    }
    return render(request, 'core/stripe-payment-success.html', context)


def stripe_payment_cancelled(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'core/stripe-confirmation.html', context)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

        # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  # contains a stripe.PaymentIntent

        if session.payment_status == 'paid':
            line_item = session.list_line_items(session.id, limit=1).data[0]
            course_id = line_item['description']
            fulfill_order(course_id)

    return HttpResponse(status=200)


def fulfill_order(request, course_id):
    course = UserCourse.objects.get(slug=course_id)
    course.user = request.user

    course.save()
