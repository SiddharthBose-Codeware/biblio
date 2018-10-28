from django.contrib.auth.models import BaseUserManager
from polymorphic.managers import PolymorphicManager

import biblio.models

class AccountManager(BaseUserManager, PolymorphicManager):

    pass

class UserManager(AccountManager):

    def create_user(self, email, username, firstname, lastname, password):

        help(self.model)

        user = self.model(

            email = self.normalize_email(email),

            first_name = firstname,

            last_name = lastname,

            username = username

        )

        user.set_password(password)

        user.save()

        return user

    def create_superuser():

        pass

class AdminManager(AccountManager):

    def create_user(self, email, firstname, lastname, libraryData, password):

        user = self.model(

            email = self.normalize_email(email),

            first_name = firstname,

            last_name = lastname,

            library = biblio.models.Library.objects.create(**libraryData)

        )

        user.set_password(password)

        user.save()

        return user

    def create_superuser():

        pass
