from django.db import models


class Subject:
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
            observer.update(self)


class Logger(models.Model, Subject):
    def save(self):
        super()
        self.notify()  # notify all observers
