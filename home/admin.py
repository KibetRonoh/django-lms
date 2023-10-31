from django.contrib import admin
from .models import Contact, Testimonial, Faq, Term, Privacy, Refund


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'message', 'contact_date')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description', 'featured', 'created_date')


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'belongs')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    pass


@admin.register(Privacy)
class TermAdmin(admin.ModelAdmin):
    pass

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    pass
