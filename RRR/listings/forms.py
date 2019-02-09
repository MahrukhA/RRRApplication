from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = [
			'title',
			'location',
			'description',
			'daily_price',
			'photo_1',
			'photo_2',
			'photo_3',
			'photo_4',
			'photo_5',
		]