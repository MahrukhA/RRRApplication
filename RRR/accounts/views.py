from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from listings.models import Listing
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        # create variables for the form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # passwords check
        if password == password2:
            # check for existing username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                return redirect('register')
            else:
                # check for existing emails
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken!')
                    return redirect('register')
                else:
                    # register the user
                    user = User.objects.create_user(first_name=first_name,
                                                    last_name=last_name,
                                                    username=username,
                                                    email=email,
                                                    password=password)
                    user.save()
                    messages.success(request, 'Registration successful!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords must match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # user found in database
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'User not found!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    user_listings_query = Listing.objects.filter(
        user_id=request.user).order_by('id')
    paginator = Paginator(user_listings_query, 10)
    page = request.GET.get('page')
    user_listings = paginator.get_page(page)
    return render(request, 'accounts/dashboard.html', {'user_listings': user_listings})


def profile(request):
    return render(request, 'accounts/profile.html')
