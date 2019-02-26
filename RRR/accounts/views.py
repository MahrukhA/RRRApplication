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
    if request.user.is_authenticated is False: #User must be logged in to view their Edit Profile page
        messages.error(request, 'You must be logged in to view this page!')
        return redirect('login')

    user_account = User.objects.get(id=request.user.id)
    context = {
        'first_name': user_account.first_name,
        'last_name': user_account.last_name,
        'username': user_account.username,
        'email': user_account.email,
    }

    if request.method == 'POST': #User changed their info
        first_name = request.POST.get('first_name', 0)
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password', 0)
        confirm_new_password = request.POST.get('confirm_new_password', 0)
        old_password = request.POST.get('old_password', "blank")

        if not (first_name and last_name and username and email and old_password): #one or more required fields left blank
            messages.error(request, 'Only the new passworld fields can be left blank! Please try again')
            return render(request, 'accounts/profile.html', context)

        if confirm_new_password != new_password: #new password and confirm new password didnt match
            messages.error(request, 'New password fields did not match! Please try again')
            return render(request, 'accounts/profile.html', context)

        check_password = auth.authenticate(username=request.user.username, password=old_password) #true when old_password matches the users actual password

        if check_password is None: #User entered an incorrect password 
            messages.error(request, 'Invalid password! Please try again.')
            return render(request, 'accounts/profile.html', context)


        
        if User.objects.filter(username=username).exists() and (username != context['username']): # username already exists
            messages.error(request, 'Username already taken!')
            return render(request, 'accounts/profile.html', context)

        if User.objects.filter(email=email).exists() and (email != context['email']): #email already exists
            messages.error(request, 'Email already taken!')
            return render(request, 'accounts/profile.html', context)

        #Update account information
        user_account.first_name = first_name
        user_account.last_name = last_name
        user_account.username = username
        user_account.email = email

        #update the context to display the updated details when the profile page reloads
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['username'] = username
        context['email'] = email



        if new_password: #Update password only if a new one was entered
            user_account.set_password(new_password)

        user_account.save()
        messages.success(request, 'Info successfully updated!')

        if new_password: #Must re-login if a new password has been set, or you will be logged out when updating your password
            auth.login(request, auth.authenticate(username=username, password=new_password))


    

    return render(request, 'accounts/profile.html', context)
