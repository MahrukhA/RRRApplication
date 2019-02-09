from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ListingForm


def index(request):
    return render(request, 'listings/viewlistings.html')


def listing(request):
    return render(request, 'listings/listing.html')

def create(request):
	if request.method == 'POST':

		#5 and 15 ARE PLACEHOLDER VALUES for right now
		#title is too short
		if (len(request.POST['title']) < 5):
			messages.error(request, 'Title must be at least 5 characters long!')
			return redirect('create')

		#description is too short
		if (len(request.POST['description']) < 15):
			messages.error(request, 'Description must be at least 15 characters long!')
			return redirect('create')

		#price is empty
		if (len(str(request.POST['daily_price'])) < 1):
			messages.error(request, 'Price can\'t be blank!')
			return redirect('create')

		#uploaded file must be a jpg
		#goes through all the photos (photo_1 to photo_5) and checks if they exist
		#if the photo exists (ie a user uploaded that image), it must end with .jpg, .JPG, .png, .PNG
		for i in range(1, 6):
			filepath = request.FILES.get('photo_' + str(i), False) #booleanFalse if the photo doesnt exist. If the file exists, it is equal to the name of the file (eg pairofskates.png)
			if (filepath is not ('' or False) and not (str(filepath).endswith('.jpg') or str(filepath).endswith('.JPG') or str(filepath).endswith('.png') or str(filepath).endswith('PNG'))):
				messages.error(request, 'Uploaded files must be jpgs or pngs!')
				return redirect('create')

		form = ListingForm(request.POST, request.FILES) #Stores user entered information in a form automatically 

		if form.is_valid():

			newListing = form.save(commit=False)
			newListing.user_id = request.user.id #foreign key - logged in user's ID (int)
			newListing.save()

			messages.success(request, 'Listing successfully created! It now awaits admin approval')
			return redirect('dashboard')
		
		else: #error while trying to create a post - this should never happen
			messages.error(request, 'Error! Please try again.')
			return redirect('create') 

	else:
		return render(request, 'listings/create.html') #User clicked on the Create a Listing button

