from django.contrib import admin
from .models import User, InstructorApplication, Socials


# Showing tables in admin
class InstructorApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'message', 'status')


admin.site.register(User)
admin.site.register(Socials)
admin.site.register(InstructorApplication, InstructorApplicationAdmin)