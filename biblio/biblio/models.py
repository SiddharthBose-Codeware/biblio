from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from polymorphic.models import PolymorphicModel

from biblio.managers import *

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

class LibrarySubjectType(models.Model):

     parent = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)

     type = models.CharField(max_length = 200, default = "", unique = True)

class LibraryAuthor(models.Model):

    name = models.CharField(max_length = 200, default = "")

class LibraryItemType(PolymorphicModel):

    type = models.CharField(max_length = 200, default = "", null = True)

class LibraryBookItemType(LibraryItemType):

    pass

class LibraryItem(PolymorphicModel):

    name = models.CharField(max_length = 400, default = "")

    author = models.ForeignKey('LibraryAuthor', on_delete = models.CASCADE)

    itemType = models.ForeignKey('LibraryItemType', on_delete = models.CASCADE)

    subjectType = models.ForeignKey('LibrarySubjectType', on_delete = models.CASCADE)

class LibraryBookItem(LibraryItem):

    ISBNCode = models.BigIntegerField(default = "")

class LibraryItemIssue(models.Model):

    item = models.ForeignKey('LibraryItem', on_delete = models.CASCADE)

    issuedToUser = models.ForeignKey('UserAccount', on_delete = models.CASCADE)

    issuedAt = models.DateField(auto_now = True)

    returnDate = models.DateField()

class Library(models.Model):

    name = models.CharField(max_length = 1000, default = "")

    subjectTypes = models.ManyToManyField('LibrarySubjectType')

    authors = models.ManyToManyField('LibraryAuthor')

    itemTypes = models.ManyToManyField('LibraryItemType')

    items = models.ManyToManyField('LibraryItem')

    issues = models.ManyToManyField('LibraryItemIssue')

    users = models.ManyToManyField('UserAccount')

    def addSubjectType(self, type, parent = None, isRoot = False):

        print(type)

        subjectType = LibrarySubjectType()

        subjectType.type = type

        if not isRoot:

            subjectType.parent = parent

        subjectType.save()

        self.subjectTypes.add(subjectType)

        return subjectType

    def addAuthor(self, authorName):

        author = LibraryAuthor()

        author.name = authorName

        author.save()

        self.authors.add(author)

        return author

    def addItemType(self, type = None, isBookItemType = False):

        item = None

        if isBookItemType:

            item = LibraryItemType()

            item.type = "Book"

        else:

            item = LibraryBookItemType()

            item.type = type

        item.save()

        self.itemTypes.add(item)

        return item

    def addItem(self, data, isBook = False):

        item = None

        if isBook:

            item = LibraryBookItem()

            item.name = data['name']
            item.author = data['author']
            item.itemType = data['itemType']
            item.subjectType = data['subjectType']
            item.ISBNCode = data['ISBNCode']

        else:

            item = LibraryItem()

            item.name = data['name']
            item.author = data['author']
            item.itemType = data['itemType']
            item.subjectType = data['subjectType']

        item.save()

        self.items.add(item)

        return item

    def addLibraryItemIssue(self, data):

        issue = LibraryItemIssue()

        print(data)

        issue.item = data['item']

        issue.issuedToUser = data['issuedToUser']

        issue.returnDate = data['returnDate']

        issue.save()

        self.issues.add(issue)

        return issue

    def addUser(self, data):

        user = data['user']

        self.users.add(user)

        return user

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
            self.email = data['email']
        if 'password' in data:
            self.set_password(data['password']) # Creating argon2 password hasher object and hashing the password

        self.save()

class AdminAccount(Account):

    objects = AdminManager()

    library = models.ForeignKey('Library', on_delete = models.PROTECT)

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
