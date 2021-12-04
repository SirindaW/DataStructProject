from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

from .forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm

# Create your views here.


def register_view(request):
    # if user is logged in; redirect
    if request.user.is_authenticated:
        return redirect('profile_view')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email,password = raw_password)
            login(request,account)
            messages.success(request,f'Account created for {form.cleaned_data.get("email")}.')
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)

def login_view(request):
    # if user is logged in; redirect
    if request.user.is_authenticated:
        return redirect('profile_view')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    

    context = {
        'form' :form
    }
    return render(request,'login.html',context)

def profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login_view')

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            print("SOMETHING")
            form.save()
    else:
        form = AccountUpdateForm()
        

    user = request.user

    context = {
        'user':user,
        'form':form,
    }
    return render(request,'profile.html',context)

def logout_view(request):
    logout(request)
    return redirect('login_view')