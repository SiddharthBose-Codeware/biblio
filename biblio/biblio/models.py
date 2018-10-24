from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from polymorphic.models import PolymorphicModel

from biblio.usersmanager import *

# class Account(AbstractBaseUser):
#     # first_name = models.CharField(max_length = 255, default = "")
#     # last_name = models.CharField(max_length = 255, default = "")
#     # email = models.CharField(max_length = 255, default = "")
#     # password = models.CharField(max_length = 255, default = "")
#
#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False)
#     admin = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'

class Account(AbstractBaseUser, PolymorphicModel):

    objects = AccountManager()

    first_name = models.CharField(max_length = 255, default = "")

    last_name = models.CharField(max_length = 255, default = "")

    email = models.CharField(max_length = 255, default = "", unique = True)

    password = models.CharField(max_length = 1000, default = "")

    USERNAME_FIELD = 'email'

    def update(self, data):

        if 'firstname' in data:
            self.first_name = data['firstname']
        if 'lastname' in data:
            self.last_name = data['lastname']
        if 'email' in data:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\nMadPerson\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self.email = data['email']
        if 'password' in data:
            self.set_password(data['password']) # Creating argon2 password hasher object and hashing the password

        self.save()

class AdminAccount(Account):

    objects = AdminManager()

    library = models.ForeignKey(Library, on_delete = models.PROTECT)

    def update(self, data):

        super(AdminAccount, self).update(data)

        if 'libraryname' in data:
            self.library.name = data['libraryname']
            self.library.save()

        self.save()

class UserAccount(Account):

    objects = UserManager()

    username = models.CharField(max_length = 255, default = "")

    def update(self, data):

        super(UserAccount, self).update(data)

        if 'libraryname' in data:
            self.library.name = data['libraryname']
            self.library.save()

        self.save()

class LibrarySubjectType(models.Model):

     parent = models.ForeignKey(self, null = True)

     itemTypeValue = models.CharField(max_length = 200, default = "")

class LibraryAuthor(models.Model):

    name = models.CharField(max_length = 200, default = "")

class LibraryItem(models.Model):

    itemName = models.CharField(max_length = 200, default = "")

    subject = models.OneToOneField(LibrarySubjectType)

    author = models.OneToOneField(LibraryAuthor)

class Library(models.Model):

    name = models.CharField(max_length = 1000, default = "")

    subjectTypes = models.ManyToManyField(LibrarySubjectType, null = True)

    authors = models.OneToOneField(LibraryAuthor, null = True)

    libraryItems = models.ManyToManyField(LibraryItem, null = True)
