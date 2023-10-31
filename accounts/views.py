from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.models import InstructorApplication, Socials
from core.models import Category, UserCourse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from settings.models import SiteSetting
User = get_user_model()


# This is registration view for user sign up
def register(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    context = {
        'categories': categories,
        'settings': settings,
    }
    # Checking if method is post or get
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # checking the length of password and making sure it is between 6-15 words
        if(len(password) >= 6 and len(password) < 15): # if 6 < len(password) < 15:
            # Check if passwords match
            if password == password2:
                # Check if username has been used already
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That username is taken')
                    return redirect('register')
                else:
                    # Check if email has been used already
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'That email is being used')
                        return redirect('register')
                    else:
                        # if all is well, then save details to db
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name)
                        # Login after register
                        # auth.login(request, user)
                        # messages.success(request, 'You are now logged in')
                        # return redirect('index')
                        user.save()
                        messages.success(request, 'You are now registered and can log in')
                        return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
        else:
            messages.error(request, 'Passwords must be 6 - 15 characters long')
            return redirect('register')
    else:
        return render(request, 'registration/register.html', context)


def login(request):
    # getting user settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    context = {
        'categories': categories,
        'settings': settings,
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        # check if user exists
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'registration/login.html', context)

@login_required
def profile(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    # getting and counting user specific enrolled courses
    my_course_count = UserCourse.objects.filter(user=request.user).count()
    context = {
        'categories': categories,
        'settings': settings,
        'my_course_count': my_course_count,
    }
    return render(request, 'registration/profile.html', context)

# dashboard view
@login_required
def dashboard(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    # getting user specific competed courses
    completed_courses = UserCourse.objects.filter(user=request.user, has_completed=True)
    # getting user specific active courses
    active_courses = UserCourse.objects.filter(user=request.user, has_completed=False)
    # getting user specific enrolled courses
    my_courses = UserCourse.objects.filter(user=request.user)
    # counting all user specific  enrolled courses
    my_course_count = UserCourse.objects.filter(user=request.user).count()

    context = {
        'categories': categories,
        'settings': settings,
        'completed_courses': completed_courses,
        'active_courses': active_courses,
        'my_courses': my_courses,
        'my_course_count': my_course_count,
    }
    return render(request, 'accounts/dashboard.html', context)


# updating profile
@login_required
def profile_update(request):
    # checking form method
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        age = request.POST['age']
        email = request.POST['email']
        password = request.POST['password']
        bio = request.POST['bio']
        user_image = request.FILES['user_image']

        # getting currently logged in user
        user_id = request.user.id

        # updating details
        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.age = age
        user.email = email
        user.bio = bio
        user.user_image = user_image
        # checking if password is not empty
        if password != None and password != '':
            user.set_password(password)

        user.save()
        messages.success(request, 'Profile successfully updated')
    return redirect('profile')


# logout view
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')


# instructor registration form
def become_instructor(request):
    # getting the currently logged in user
    user_id = request.user.id

    user = User.objects.get(id=user_id)
    settings = SiteSetting.objects.all()
    categories = Category.objects.all().order_by('id')[0:6]

    context = {
        'settings': settings,
        'user': user,
        'categories': categories,
    }
    # checking for method
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']

        # checking if user has already applied to become instructor
        if InstructorApplication.objects.filter(email=email).exists():
            messages.error(request, 'You have already applied, wait for admin to approve')
            return redirect('become-instructor')
        else:
            # if everything is okay then save the application
            instructors = InstructorApplication(first_name=first_name, last_name=last_name, applicant=request.user,
                                            email=email, phone_number=phone_number, message=message)
            instructors.save()
    return render(request, 'accounts/become-instructor.html', context)


def student_details(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    # getting the currently logged in user
    user = User.objects.get(id=request.user.id)
    # counting all the courses of currently logged in user
    my_course_count = UserCourse.objects.filter(user=request.user).count()

    context = {
        'user': user,
        'settings': settings,
        'categories': categories,
        'my_course_count': my_course_count,
    }
    return render(request, 'accounts/student-details.html', context)


def user_socials(request):
    # getting settings
    settings = SiteSetting.objects.all()
    # getting categories
    categories = Category.objects.all().order_by('id')[0:6]
    # getting the currently logged in user
    user = User.objects.get(id=request.user.id)
    # counting all the courses of currently logged in user
    my_course_count = UserCourse.objects.filter(user=request.user).count()

    context = {
        'settings': settings,
        'user': user,
        'categories': categories,
        'my_course_count': my_course_count,
    }
    # updating user social links
    if request.method == 'POST':
        facebook = request.POST['facebook']
        x = request.POST['x']
        youtube = request.POST['youtube']
        instagram = request.POST['instagram']

        socials = Socials(user=user, facebook=facebook, x=x, youtube=youtube, instagram=instagram)
        socials.save()
    return render(request, 'registration/profile.html', context)

