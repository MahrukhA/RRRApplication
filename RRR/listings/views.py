from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ListingForm
from .models import Listing
from django.core.paginator import Paginator

def index(request):
	query = request.GET.get('q')#search query (= None if q POST var isnt set)
	if query is not None:
		approved_listings_query = Listing.objects.filter(is_approved = True, title__icontains=query).order_by('id') #gets all approved listings, and sorts by id in ascending order
	else:
		approved_listings_query = Listing.objects.filter(is_approved = True).order_by('id')#query wasn't entered - display ALL approved listings
	
	available = request.GET.get('available')
	if available is not None:
		approved_listings_query = approved_listings_query.filter(is_available = True)

	daily_price = request.GET.get('daily_price')
	if daily_price is not None:
		daily_price = int(daily_price)
		if daily_price == 0:
			approved_listings_query = approved_listings_query.filter(daily_price__range=(0, 14))
		elif daily_price == 1:
			approved_listings_query = approved_listings_query.filter(daily_price__range=(15, 30))
		elif daily_price == 2:
			approved_listings_query = approved_listings_query.filter(daily_price__range=(31, 50))
		elif daily_price == 3:
			approved_listings_query = approved_listings_query.filter(daily_price__range=(51, 75))
		else:
			approved_listings_query = approved_listings_query.filter(daily_price__range=(76, 1000))

	location = request.GET.get('location')
	if location is not None:
		location = int(location)
		if location == 0:
			approved_listings_query = approved_listings_query.filter(location = 0)
		elif location == 1:
			approved_listings_query = approved_listings_query.filter(location = 1)
		elif location == 2:
			approved_listings_query = approved_listings_query.filter(location = 2)
		else:
			approved_listings_query = approved_listings_query.filter(location = 3)

	paginator = Paginator(approved_listings_query, 3) #3 listings per page
	page = request.GET.get('page') #gets page number from url
	approved_listings = paginator.get_page(page) #gets the approved listings from some page number
	return render(request, 'listings/viewlistings.html', {'approved_listings': approved_listings, 'count': approved_listings_query.count, 'query': query})


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
		#can only view the create a listing page if they are logged in
		if not request.user.is_authenticated:
			#create a listing redirects to login when not logged in, so this redirect will happen when users type in the url for the create page instead of clicking on the button
			messages.error(request, 'Must be logged in to create a listing!')
			return redirect('login')
		else:
			return render(request, 'listings/create.html') #logged in user clicked on the Create a Listing button

