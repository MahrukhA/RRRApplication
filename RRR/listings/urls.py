from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    # following will look like /viewlistings/1 or index of specific listing
    path('<int:listing_id>', views.listing, name='listing'),
]
