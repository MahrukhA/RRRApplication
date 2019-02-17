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
