from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django_postgres_extensions.models.functions import ArrayRemove, ArrayAppend


class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.IntegerField()
    description = models.TextField()
    daily_price = models.IntegerField()
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    subscribers = ArrayField(
        models.EmailField(blank=True),
        default=list,
        blank=True,
    )

    class Meta:
        db_table = 'listings_listing'  # table name

    def __str__(self):
        return self.title

    def register(self, observer):
        if observer not in self.subscribers:
            self.subscribers = ArrayAppend('subscribers', observer)
            super(Listing, self).save()
        else:
            print('email already exists in database!')
    
    def remove(self, observer):
        try:
            self.subscribers = ArrayRemove('subscribers', observer)
            super(Listing, self).save()
        except ValueError:
            print('failed to remove email!')

    # def notify(self):
    #     for observer in self.subscribers:
    #         observer.update()

    # def save(self):
    #     super(ListingData, self).save()
    #     self.notify()  # notify all observers..?