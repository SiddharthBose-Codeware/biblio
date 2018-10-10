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
