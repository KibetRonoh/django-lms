from django.contrib import admin
from .models import Category, Author, Course, Level, WhatToLearn, Requirement, Section, Video, Language, UserCourse, Subscription, Order, Features, Review
from django.contrib.auth import get_user_model
User = get_user_model()
# from django_summernote.admin import SummernoteModelAdmin


# adding what to learn as tabular Inline
class WhatToLearnTabularInline(admin.TabularInline):
    model = WhatToLearn


class RequirementsTabularInline(admin.TabularInline):
    model = Requirement


class VideoTabularInline(admin.TabularInline):
    model = Video


class FeaturesTabularInline(admin.TabularInline):
    model = Features


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [FeaturesTabularInline]


class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatToLearnTabularInline, RequirementsTabularInline, VideoTabularInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'points')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscription', 'created')
    list_per_page = 25


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'user', 'course', 'rating', 'comment', 'rating_date')


# class SummerAdmin(SummernoteModelAdmin):
#     summernote_fields = '__all__'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
admin.site.register(Course, CourseAdmin)
admin.site.register(Level)
admin.site.register(WhatToLearn)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Section)
admin.site.register(Video)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Features)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment)
