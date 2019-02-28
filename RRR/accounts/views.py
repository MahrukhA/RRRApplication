from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from listings.models import Listing
from django.core.paginator import Paginator
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': form})


def dashboard(request):
    user_listings_query = Listing.objects.filter(user_id=request.user).order_by('id')
    paginator = Paginator(user_listings_query, 10)
    page = request.GET.get('page')
    user_listings = paginator.get_page(page)

    if request.method == 'POST':
        specific_listing = Listing.objects.get(id=request.POST['set_rented'])
        if specific_listing.is_available is True:
            specific_listing.is_available = False
            specific_listing.save()
            messages.warning(request, '{0} will no longer be shown as available!'.format(specific_listing))
        else:
            specific_listing.is_available = True
            specific_listing.save()
            specific_listing.notify()
            messages.success(request, '{0} will now be available for others to rent! Subscribers will also be notified.'.format(specific_listing))

    return render(request, 'accounts/dashboard.html', {'user_listings_query': user_listings_query, 'user_listings': user_listings})


def profile(request):
    if request.user.is_authenticated is False:  # User must be logged in to view their Edit Profile page
        messages.error(request, 'You must be logged in to view this page!')
        return redirect('login')

    user_account = User.objects.get(id=request.user.id)
    context = {
        'first_name': user_account.first_name,
        'last_name': user_account.last_name,
        'username': user_account.username,
        'email': user_account.email,
    }

    if request.method == 'POST':  # User changed their info
        first_name = request.POST.get('first_name', 0)
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password', 0)
        confirm_new_password = request.POST.get('confirm_new_password', 0)
        old_password = request.POST.get('old_password', "blank")

        # one or more required fields left blank
        if not (first_name and last_name and username and email and old_password):
            messages.error(request, 'Only the new passworld fields can be left blank! Please try again')
            return render(request, 'accounts/profile.html', context)

        if confirm_new_password != new_password:  # new password and confirm new password didnt match
            messages.error(request, 'New password fields did not match! Please try again')
            return render(request, 'accounts/profile.html', context)

        # true when old_password matches the users actual password
        check_password = auth.authenticate(username=request.user.username, password=old_password)

        if check_password is None:  # User entered an incorrect password
            messages.error(request, 'Invalid password! Please try again.')
            return render(request, 'accounts/profile.html', context)

        # username already exists
        if User.objects.filter(username=username).exists() and (username != context['username']):
            messages.error(request, 'Username already taken!')
            return render(request, 'accounts/profile.html', context)

        # email already exists
        if User.objects.filter(email=email).exists() and (email != context['email']):
            messages.error(request, 'Email already taken!')
            return render(request, 'accounts/profile.html', context)

        # Update account information
        user_account.first_name = first_name
        user_account.last_name = last_name
        user_account.username = username
        user_account.email = email

        # update the context to display the updated details when the profile page reloads
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['username'] = username
        context['email'] = email

        if new_password:  # Update password only if a new one was entered
            user_account.set_password(new_password)

        user_account.save()
        messages.success(request, 'Info successfully updated!')

        if new_password:  # Must re-login if a new password has been set, or you will be logged out when updating your password
            auth.login(request, auth.authenticate(
                username=username, password=new_password))

    return render(request, 'accounts/profile.html', context)
