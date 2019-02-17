from abc import ABCMeta, abstractmethod
# https://codereview.stackexchange.com/questions/20938/the-observer-design-pattern-in-python-in-a-more-pythonic-way-plus-unit-testing


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


class ListingData(Subject):
    # Concrete Subject
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
