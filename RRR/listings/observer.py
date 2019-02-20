from abc import ABCMeta, abstractmethod
from .models import Listing
from django.contrib.auth.models import User


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


class ConcreteObserver(User, Observer):
    class Meta:
        proxy = True

    def update(self, subject):
        print('observer was notified successfully about the availability of {0}'.format(
            subject))


class ListingData(Listing, Subject):
    class Meta:
        proxy = True

    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            print('Failed to add: {}'.format(observer))

    def remove(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            print('Failed to remove: {}'.format(observer))

    def notify(self):
        for observer in self._observers:
            observer.update()

    def save(self):
        super(ListingData, self).save()
        self.notify()  # notify all observers
