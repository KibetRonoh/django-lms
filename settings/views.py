from django.shortcuts import render


def site_setting(request):
    return render(request, 'settings/site.html')