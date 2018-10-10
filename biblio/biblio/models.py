from django.db import models

class Account(models.Model):

    def __init__(self):
        self.firstname = models.CharField(max_length = 255)
        self.lastname = models.CharField(max_length = 255)
        self.email = models.TextField(max_length = 500)
        self.password = models.CharField(max_length = 255)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

class AdminAccount(Account):
    def __init__(self):
        super(self.__class__, self).__init__()
        # Add library ID here later

class UserAccount(Account):
    def __init__(self):
        super(self.__class__, self).__init__()
        userId = models.CharField(max_length = 50)
