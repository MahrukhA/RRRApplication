from abc import ABCMeta, abstractmethod
from .models import Listing
from django.contrib.auth.models import User
from django_postgres_extensions.models.functions import ArrayRemove, ArrayAppend


# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#extending-the-existing-user-model


class Subject:
    # Interface Subject (technically abstract...)
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, observer):
        """Registers an observer with Subject."""
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
    # Interface Observer (technically abstract...)
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        """Observer updates by pulling data from Subject."""
        pass


# class ConcreteObserver(User, Observer):
#     class Meta:
#         proxy = True

#     def update(self, subject):
#         print('observer was notified successfully about the availability of {0}'.format(subject))
