from rest_framework import serializers
from biblio.models import *
import secrets
import argon2
import datetime
from api.modelfunctions import *
from rest_framework.fields import CurrentUserDefault


class AccountSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validateRequest(request):

        for each in ['firstname', 'lastname', 'libraryname', 'email', 'password']:

            if each not in request.POST:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        exsistingAccountsWithGivenEmail = Account.objects.filter(email = request.POST['email'])

        if len(exsistingAccountsWithGivenEmail) != 0:

            return {

                'message': 'Account with the email \"' + str(request.POST['email']) + '\" already exsists'

            }

        return True

class UserAccountSerializer(AccountSerializer):

    username = serializers.CharField()

    def validateRequest(request):

        for each in ['firstname', 'lastname', 'username', 'email', 'password']:

            if each not in request.POST:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        exsistingAccountsWithGivenEmail = Account.objects.filter(email = request.POST['email'])

        if len(exsistingAccountsWithGivenEmail) != 0:

            return {

                'message': 'Account with the email \"' + str(request.POST['email']) + '\" already exsists'

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

            if each not in request.POST:

                return {

                    'message': 'Missing info \'' + each + "\'"

                }

        exsistingAccountsWithGivenEmail = Account.objects.filter(email = request.POST['email'])

        if len(exsistingAccountsWithGivenEmail) != 0:

            return {

                'message': 'Account with the email \"' + str(request.POST['email']) + '\" already exsists'

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

class LibrarySubjectTypeSerializer(serializers.ModelSerializer):

    parentType = serializers.SerializerMethodField(source = "get_parentType")

    class Meta:

        model = LibrarySubjectType

        fields = ('type', 'parent', 'id', 'parentType')

    def get_parentType(self, object):

        if object.parent is not None:

            parent = LibrarySubjectType.objects.filter(pk = object.parent.pk)[0]

            return parent.type

        return None

    def create(self, data):

        # user = None

        print(data)

        user = self.context.get("request").user

        # request = self.context.get("request")

        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(request)

        # if request and hasattr(request, "user"):
        #     user = request.user

        if 'parent' in data:

            return user.library.addSubjectType(type = data['type'], parent = data['parent'])

        else:

            return user.library.addSubjectType(type = data['type'], isRoot = True)

    def partial_update(self, instance, validated_data):

        if 'type' in validated_data:

            instance.type = validated_data['type']

        if 'parent' in validated_data:

            instance.parent = validated_data['parent']

        instance.save()

        return instance


class LibraryAuthorSerializer(serializers.ModelSerializer):

    class Meta:

        model = LibraryAuthor

        fields = ('name', 'id')

    def create(self, data):

        # user = None

        user = self.context.get("request").user

        # request = self.context.get("request")

        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(request)

        # if request and hasattr(request, "user"):
        #     user = request.user

        return user.library.addAuthor(authorName = data['name'])

    def partial_update(self, instance, validated_data):

        print(validated_data)

        if 'name' in validated_data:

            instance.name = validated_data['name']

        instance.save()

        return instance

class LibraryItemTypeSerializer(serializers.ModelSerializer):

    # def to_representation(self, instance):
    #
    #     if isinstance(instance, LibraryBookItemType):
    #
    #         return LibraryBookItemTypeSerializer(instance = instance).data
    #
    #     return LibraryItemTypeSerializer(instance = instance).data

    class Meta:

        model = LibraryItemType

        fields = '__all__'

    def create(self, data):

        # user = None

        user = self.context.get("request").user

        # request = self.context.get("request")

        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(request)

        # if request and hasattr(request, "user"):
        #     user = request.user

        return user.library.addItemType(type = data['type'], isBookItemType = False)

    def partial_update(self, instance, validated_data):

        if 'type' in validated_data:

            instance.type = validated_data['type']

        instance.save()

        return instance

class LibraryBookItemTypeSerializer(LibraryItemTypeSerializer):

    def create(self, data):

        # user = None

        user = self.context.get("request").user

        # request = self.context.get("request")

        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(request)

        # if request and hasattr(request, "user"):
        #     user = request.user

        return user.library.addItemType(isBookItemType = True)

# class LibraryItemTypeSerializer(serializers.ModelSerializer):
#
#     def to_representation(self, instance):
#
#         if isinstance(instance, LibraryBookItemType):
#
#             print("Book")
#
#             return LibraryBookItemTypeSerializer(instance = instance)
#
#         print("Non - Book")
#
#         return LibraryItemTypeSerializer(instance = instance)
#
#     class Meta:
#
#         model = LibraryBookItemType
#
#         fields = '__all__'

class LibraryItemSerializer(serializers.ModelSerializer):

    authorName = serializers.SerializerMethodField(source = 'get_authorName')

    itemTypeName = serializers.SerializerMethodField(source = 'get_itemTypeName')

    subjectTypeName = serializers.SerializerMethodField(source = 'get_subjectTypeName')

    class Meta:

        model = LibraryItem

        fields = ('id', 'name', 'author', 'itemType', 'subjectType', 'authorName', 'itemTypeName', 'subjectTypeName')

    def get_authorName(self, object):

        if object.author is not None:

            author = LibraryAuthor.objects.filter(pk = object.author.pk)[0]

            return author.name

        return None

    def get_itemTypeName(self, object):

        if object.itemType is not None:

            itemType = LibraryItemType.objects.filter(pk = object.itemType.pk)[0]

            return itemType.type

        return None

    def get_subjectTypeName(self, object):

        if object.subjectType is not None:

            subjectType = LibrarySubjectType.objects.filter(pk = object.subjectType.pk)[0]

            return subjectType.type

    def create(self, data):

        # user = None

        user = self.context.get("request").user

        # request = self.context.get("request")

        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(request)

        # if request and hasattr(request, "user"):
        #     user = request.user

        # help(user.library)

        return user.library.addItem(data = data, isBook = False)

    def partial_update(self, instance, validated_data):

        if 'name' in validated_data:

            instance.name = validated_data['name']

        if 'author' in validated_data:

            instance.author = Author.objects.filter(pk = validated_data['author'])[0]

        if 'itemType' in validated_data:

            instance.itemType = LibraryItemType.objects.filter(pk = validated_data['itemType'])[0]

        if 'subjectType' in validated_data:

            instance.subjectType = LibrarySubjectType.objects.filter(pk = validated_data['subjectType'])[0]

        instance.save()

        return instance

class LibraryBookItemSerializer(LibraryItemSerializer):

    class Meta:

        model = LibraryItem

        fields = ('name', 'author', 'itemType', 'subjectType')

    def create(self, data):

        user = self.request.user

        return user.library.addBookItem(data = data, isBook = True)

    def partial_update(self, instance, validated_data):

        if 'ISBNCode' in validated_data:

            instance.ISBNCode = validated_data['ISBNCode']

        return super(LibraryBookItemSerializer, self).partial_update(instance, validated_data)

class LibraryItemIssueSerializer(serializers.ModelSerializer):

    issuedToUserName = serializers.SerializerMethodField(source = "get_issuedToUserName")

    itemName = serializers.SerializerMethodField(source = "get_itemName")

    class Meta:

        model = LibraryItemIssue

        fields = ('issuedAt', 'issuedToUserName', 'itemName', 'issuedToUser', 'item', 'returnDate',)

    def get_issuedToUserName(self, object):

        return object.issuedToUser.username

    def get_itemName(self, object):

        return object.item.name

    def create(self, data):

        user = self.context.get("request").user

        return user.library.addLibraryItemIssue(data = data)

class LibrarySerializer(serializers.ModelSerializer):

    class Meta:

        model = Library

        isUserPresent = serializers.SerializerMethodField(source = 'get_isUserPresent')

        fields = ('name', 'isUserPresent')

    def get_isUserPresent(self, object):

        if object in self.request.user.library_set():

            return True

        return False

class UserAccountModelSerializer(serializers.ModelSerializer):

    model = UserAccount

    fields = '__all__'

    def get_queryset():

        def get_queryset(request):

            return request.user.library.users
