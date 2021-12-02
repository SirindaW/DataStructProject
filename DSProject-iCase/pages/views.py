from django.shortcuts import render


# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "main.html", {})

def test_view(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def about_view(request):
    return render(request, 'aboutus.html')

def profile_view(request):
    return render(request, 'profile.html')

def cart_view(request):
    return render(request, 'cart.html')