from rest_framework import serializers
from biblio.models import *
import secrets
import argon2
import datetime
from api.modelfunctions import *


class AccountSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validateRequest(request):

        for each in ['firstname', 'lastname', 'libraryname', 'email', 'password']:

            if each not in request.GET:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        return True

class UserAccountSerializer(AccountSerializer):

    username = serializers.CharField()

    def validateRequest(request):

        for each in ['firstname', 'lastname', 'username', 'email', 'password']:

            if each not in request.GET:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        return True

    def create(self, data):

        data['password'] = argon2.PasswordHasher().hash(data['password']) # Creating argon2 password hasher object and hashing the password

        return UserAccount.objects.create_user(**data)

    def update(self, instance, data):

        if 'firstname' in data:
            instance.firstname = data['firstname']
        if 'lastname' in data:
            instance.lastname = data['lastname']
        if 'email' in data:
            instance.firstname = data['email']
        if 'password' in data:
            instance.password = argon2.PasswordHasher(data['password']).hash() # Creating argon2 password hasher object and hashing the password
        if 'username' in data:
            instance.username = data['username']

        instance.save()

class AdminAccountSerializer(AccountSerializer):

    libraryname = serializers.CharField()

    def validateRequest(request):

        for each in ['firstname', 'lastname', 'libraryname', 'email', 'password']:

            if each not in request.GET:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        accountsWithTheGivenEmail = AdminAccount.objects.filter(email = request.GET['email'])

        if len(accountsWithTheGivenEmail) != 0:

            return {

                'message': 'Account with the email already exists.'

            }

        return True

    def create(self, data):

        libraryData = {

            'name': data['libraryname'],

        }

        adminData = {

            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'email': data['email'],
            'password': data['password'], # Creating argon2 password hasher object and hashing the password
            'libraryData': libraryData

        }

        return AdminAccount.objects.create_user(**adminData)

    def update(self, instance, data):

        if 'firstname' in data:
            instance.firstname = data['firstname']
        if 'lastname' in data:
            instance.lastname = data['lastname']
        if 'email' in data:
            instance.firstname = data['email']
        if 'password' in data:
            instance.password = argon2.PasswordHasher(data['password']).hash() # Creating argon2 password hasher object and hashing the password
        if 'username' in data:
            instance.username = data['username']

        instance.save()
