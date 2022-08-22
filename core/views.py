from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile

# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request, 'core/index.html')

def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if len(username)<4:
            messages.info(request, 'username is too sort')
            return redirect('signup')
        if len(password)<7:
            messages.info(request, 'password must be at least 8 character')
            return redirect('signup')

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password = password)
                user.save()

                #log use in and redirect to setting page

                #create a profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password is not Matching')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')
def signin(request):
    #if request.user.is_authenticated:
	    #return redirect('index')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signin')
    else:
        return render(request, 'core/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')