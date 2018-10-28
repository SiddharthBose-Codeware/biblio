import secrets
import argon2

from biblio.models import *

from biblio.managers import AdminManager, UserManager

from biblio import settings

class Accounts:

    def getAdminAccountObject(data):

        adminAccount = AdminAccount()

        adminAccount.first_name = data['firstname']
        adminAccount.last_name = data['lastname']
        adminAccount.email = data['email']
        adminAccount.password = data['password']
        adminAccount.library = data['library']

        return adminAccount

    def login(email, password, rememberMe, isAdmin):

        usersWithTheGivenEmail = None

        if isAdmin:

            usersWithTheGivenEmail = AdminAccount.objects.filter(email = email)

        else:

            usersWithTheGivenEmail = UserAccount.objects.filter(email = email)

        if len(usersWithTheGivenEmail) == 0:

            return {

                "success": False,
                "message": "No account exists with that email"

            }

        user = usersWithTheGivenEmail[0] # Since, every user has an unique email, so the user is the first one only

        hashedPasswordFromDB = user.password

        print(user.check_password(password))
        print(password)

        if not user.check_password(password):

            return {

                "success": False,
                "message": "Password is incorrect. Please try again."

            }

        print(token)

        # loginToken = secrets.token_hex(64)
        #
        # hasher = argon2.PasswordHasher()
        #
        # hashedLoginToken = hasher.hash(loginToken)

        # LoginToken.objects.create(**loginTokenData)

        # cookieExpirationTime = None



        # if rememberMe:
        #
        #     cookieExpirationTime = 60 * 60 * 24 * 7

        # token =

        return {

            "success": True,

            "token": token

        }

    def isAdminAccount(account):

        return isinstance(account.objects, AdminManager)
