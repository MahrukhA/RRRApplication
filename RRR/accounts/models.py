from django.db import models
from abc import ABCMeta, abstractmethod

class RegistrationData:
    __metaclass__ = ABCMeta


class RegistrationRule:
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self):
        """Observer notifies subject that it has become aware of the changes."""
        pass


def register(request):
    if request.method == 'POST':
        # create variables for the form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        rules = []
        rules.append()