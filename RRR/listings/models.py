from django.db import models
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django_postgres_extensions.models.functions import ArrayRemove, ArrayAppend
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail



class Subject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, observer):
        """Registers an observer to Subject."""
        pass

    @abstractmethod
    def remove(self, observer):
        """Removes an observer from Subject."""
        pass

    @abstractmethod
    def notify(self):
        """Notifies observers that Subject data has changed."""
        pass


class Observer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        """Observer notifies subject that it has become aware of the changes."""
        pass


class ConcreteObserver(User, Observer):
    class Meta:
        proxy = True

    def update(self, subject):
        print('Subscriber {0} was notified successfully about the availability of {1}'.format(self.username, subject))


class Listing(models.Model, Subject):
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
            print('Already subscribed!')
    
    def remove(self, observer):
        try:
            self.subscribers = ArrayRemove('subscribers', observer)
            super(Listing, self).save()
        except ValueError:
            print('Failed to remove!')

    def notify(self):
        subject = '[RRR] ' + self.title + ' is now available!'
        message = 'Hey! You were subscribed to ' + self.title + ' and we just wanted to let you know it\'s now available to be rented!'
        from_email = settings.EMAIL_HOST_USER
        to_email = []
        for sub in self.subscribers:
            ConcreteObserver.objects.get(email=sub).update(self.title)
            to_email.append(sub) #adds all subscribers to the emailing list

        send_mail(subject, message, from_email, to_email, fail_silently=True) #send the email to all subscribers


