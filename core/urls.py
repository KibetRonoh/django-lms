from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('courses', views.courses, name='courses'),
    path('payment-successful', views.payment_successful, name='payment-successful'),
    path('read-cat/<int:id>', views.read_cat, name='read-cat'),
    path('favorite/<slug:slug>', views.favorite, name='favorite'),
    path('search', views.search, name='search'),
    path('subscription', views.subscription, name='subscription'),
    path('confirm-subscription/<int:id>/', views.confirm_subscription, name="confirm-subscription"),
    path('subscription-complete/', views.subscription_complete, name="subscription-complete"),
    path('404', views.page_not_found, name='404'),
    path('course/filter-data', views.filter_data, name="filter-data"),
    path('course/<slug:slug>', views.course_details, name='course_details'),
    path('checkout/<slug:slug>', views.checkout, name='checkout'),
    path('paypal-checkout/<slug:slug>', views.paypal_checkout, name='paypal-checkout'),
    path('my-courses', views.my_courses, name='my-courses'),
    path('my-reviews', views.my_reviews, name='my-reviews'),
    path('complete/', views.payment_complete, name="complete"),
    path('course/course-take/<slug:slug>', views.course_take, name='course-take'),
    path('review/<slug:slug>', views.review, name='review'),
    path('submit-review/<slug:slug>/', views.submit_review, name='submit-review'),

    path('stripe-page/<slug:slug>', views.stripe_page, name='stripe-page'),
    path('create-checkout-session/<slug:slug>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('stripe-payment-success', views.stripe_payment_success, name='stripe-payment-success'),

    path('stripe-success/<slug:slug>', views.stripe_success, name='stripe-success'),
    path('stripe-payment-cancelled', views.stripe_payment_cancelled, name='stripe-payment-cancelled'),
    path('webhook/stripe', views.my_webhook_view, name='webhook-stripe'),
]
