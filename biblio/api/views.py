from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from django.http import JsonResponse
from api.serializers import *
from api.modelfunctions import *
from rest_framework.permissions import AllowAny, IsAuthenticated

import json
import urllib

class CreateUserAccountAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        validationResult = UserAccountSerializer.validateRequest(request)

        if validationResult != True:

            return JsonResponse({

                'success': False,
                'message': validationResult['message']

            }, status = 201)

        userAccountSerializer = UserAccountSerializer(data = {

            'firstname': request.GET['firstname'],
            'lastname': request.GET['lastname'],
            'username': request.GET['username'],
            'email': request.GET['email'],
            'password': request.GET['password']

        })

        if userAccountSerializer.is_valid():

            userAccountSerializer.save()

        else:

            return JsonResponse({

                'success': False,
                'message': userAccountSerializer.errors

            })

        return JsonResponse({

            'success': True,
            'message': 'Account created successfully.'

        })

class CreateAdminAccountAPIView(APIView):

    def post(self, request):

        permission_classes = (AllowAny,)

        print("\n\n\n\n\n\n\n\n\n\n\n\nSomething\n\n\n\n\n\n\n\n")

        validationResult = AdminAccountSerializer.validateRequest(request)

        if validationResult != True:

            return JsonResponse({

                'success': False,
                'message': validationResult['message']

            }, status = 201)

        adminAccountSerializer = AdminAccountSerializer(data = {

            'firstname': request.GET['firstname'],
            'lastname': request.GET['lastname'],
            'libraryname': request.GET['libraryname'],
            'email': request.GET['email'],
            'password': request.GET['password']

        })

        if adminAccountSerializer.is_valid():

            adminAccountSerializer.save()

        else:

            return JsonResponse({

                'success': False,
                'message': adminAccountSerializer.errors

            })

        return JsonResponse({

            'success': True,
            'message': 'Account created successfully.'

        })

class UpdateAccountAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def patch(self, request):

        if Accounts.isLoggedIn(request.COOKIES):

            loggedInUser = Accounts.getLoggedInUser(request.COOKIES)

class LoginAPIView(APIView):

    permission_classes = (AllowAny,)

    def login(self, data, isAdmin):

        if 'rememberMe' not in data:

            return JsonResponse({

                'success': False,
                'message': 'Something happened from our end.'

            })

        if 'email' not in data or 'password' not in data:

            return JsonResponse({

                'success': False,
                'message': 'Some or all credentials missing.'

            })

        loginResult = Accounts.login(data['email'], data['password'], data['rememberMe'], isAdmin)

        print(loginResult)

        if loginResult['success'] != True:

            # Something happened

            return JsonResponse({

                'success': False,
                'message': loginResult['message']

            }, status = 201)

        response = JsonResponse({

            'success': True,

            'token': loginResult['token']

        })

        # if loginResult['cookieDetails']['expiry'] == None:
        #
        #     response.set_cookie(loginResult['cookieDetails']['name'], loginResult['cookieDetails']['value'])
        #
        # response.set_cookie(loginResult['cookieDetails']['name'], loginResult['cookieDetails']['value'], loginResult['cookieDetails']['expiry'])

        return response

class LoginUserAPIView(LoginAPIView):

    def post(self, request):

        return self.login({

            'email': request.GET['email'],
            'password': request.GET['password'],
            'rememberMe': request.GET['rememberMe']

        }, False)

class LoginAdminAPIView(LoginAPIView):

    def post(self, request):

        return self.login({

            'email': request.GET['email'],
            'password': request.GET['password'],
            'rememberMe': request.GET['rememberMe']

        }, True)

class UpdateAccountAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # toChange = request.GET['toChange']
        #
        # newValue = request.GET['newValue']

        request.user.update(request.GET)

        return JsonResponse({

            'success': True,
            'message': "Account details updated"

        })

class LibrarySubjectTypeView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibrarySubjectTypeSerializer

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.subjectTypes.get_queryset()

    def create(self, request, *args, **kwargs):

        # request.user.library.addSubjectType(request.GET['itemTypeValue'], request.GET['parent'])

        if 'parent' in request.GET:

            subjectTypeSerializer = self.get_serializer(data = {

                'itemTypeValue': request.GET['itemTypeValue'],
                'parent':  request.GET['parent']

            })

        else:

            subjectTypeSerializer = self.get_serializer(data = {

                'itemTypeValue': request.GET['itemTypeValue']

            })


        if subjectTypeSerializer.is_valid():

            object = subjectTypeSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Created a new subject type.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': subjectTypeSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibrarySubjectType.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'itemTypeValue': object.itemTypeValue,
            'parent': object.parent

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.GET)

        return JsonResponse({

            'status': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibrarySubjectType.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'status': True,
            'message': "The subject type has been deleted."

        })

    # def create(self, serializer):
    #
    #     help(self)
    #
    #     serializer.save(data = self.request.GET)

class LibraryAuthorView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibraryAuthorSerializer

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.authors.get_queryset()

    def create(self, request, *args, **kwargs):

        authorSerializer = self.get_serializer(data = {

            'name': request.GET['name']

        })

        if authorSerializer.is_valid():

            object = authorSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Author added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': subjectTypeSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibraryAuthor.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'name': object.name

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.GET)

        return JsonResponse({

            'status': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryAuthor.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'status': True,
            'message': "The author has been deleted."

        })

class LibraryItemTypeView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibraryItemTypeSerializer

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.itemTypes.get_queryset()

    def createItemType(self, itemTypeSerializer):

        if itemTypeSerializer.is_valid():

            object = itemTypeSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Item type added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': subjectTypeSerializer.errors

                })

    def create(self, request, *args, **kwargs):

        itemTypeSerializer = self.get_serializer(data = {

            'type': request.GET['type']

        })

        return self.createItemType(itemTypeSerializer = itemTypeSerializer)

    def partial_update(self, request, *args, **kwargs):

        object = LibraryItemType.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'type': object.type

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.GET)

        return JsonResponse({

            'status': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryItemType.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'status': True,
            'message': "The item type has been deleted."

        })

class LibraryBookItemTypeView(LibraryItemTypeView):

    serializer_class = LibraryBookItemTypeSerializer

    def get_queryset(self):

        return self.request.user.library.itemTypes.filter(type = None)

    def create(self, request, *args, **kwargs):

        itemTypeSerializer = self.get_serializer(data = {})

        help(itemTypeSerializer)

        return self.createItemType(itemTypeSerializer = itemTypeSerializer)

class LibraryItemView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibraryItemSerializer

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.items.get_queryset()

    def create(self, request, *args, **kwargs):

        itemSerializer = self.get_serializer(data = {

            'name': request.GET['name'],
            'author': request.GET['author'],
            'itemType': request.GET['itemType'],
            'subjectType': request.GET['subjectType']

        })

        if itemSerializer.is_valid():

            object = itemSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Item added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': itemSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'name': object.name

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.GET)

        return JsonResponse({

            'status': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'status': True,
            'message': "The item has been deleted."

        })

class LibraryItemView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibraryItemSerializer

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.items.get_queryset()

    def get_serializer_class(self):

        if self.request.GET['itemType'] is None:

            return LibraryBookItemSerializer

        return LibraryItemSerializer

    # def getLibraryItemSerializer(self, data):
    #
    #     if data['itemType'] is None:
    #
    #         return self.get_serializer_class(data = {
    #
    #             'name': data['name'],
    #             'author': data['author'],
    #             'itemType': data['itemType'],
    #             'subjectType': data['subjectType'],
    #             'ISBNCode': data['ISBNCode']
    #
    #         })
    #
    #     itemSerializer = self.get_serializer_class(data = {
    #
    #         'name': data['name'],
    #         'author': data['author'],
    #         'itemType': data['itemType'],
    #         'subjectType': data['subjectType']
    #
    #     })

    def createItem(self, itemSerializer):

        if itemSerializer.is_valid():

            object = itemSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Item added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': itemSerializer.errors

                })

    def create(self, request, *args, **kwargs):

        itemSerializer = None

        if request.GET['itemType'] is None:

            itemSerializer = self.get_serializer(data = {

                'name': request.GET['name'],
                'author': request.GET['author'],
                'itemType': request.GET['itemType'],
                'subjectType': request.GET['subjectType'],
                'ISBNCode': request.GET['ISBNCode']

            })

        else:

            itemSerializer = self.get_serializer(data = {

                'name': request.GET['name'],
                'author': request.GET['author'],
                'itemType': request.GET['itemType'],
                'subjectType': request.GET['subjectType']

            })

        # help(itemSerializer)

        return self.createItem(itemSerializer)

    def partial_update(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'name': object.name

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.GET)

        return JsonResponse({

            'status': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'status': True,
            'message': "The item has been deleted."

        })

class LibraryBookItemView(LibraryItemView):

    serializer_class = LibraryBookItemSerializer

    def get_queryset(self):

        return self.request.user.library.itemTypes.filter(type = None)

    def create(self, request, *args, **kwargs):

        bookItemSerializer = self.get_serializer(data = {

            'name': request.GET['name'],
            'author': request.GET['author'],
            'itemType': request.GET['itemType'],
            'subjectType': request.GET['subjectType'],
            'ISBNCode': request.GET['ISBNCode']

        })

        return self.createItem(bookItemSerializer)


class LibraryItemIssueView(viewsets.ModelViewSet):

    serializer_class = LibraryItemIssueSerializer

    def get_queryset(self):

        return self.request.user.library.issues.get_queryset()

    def createIssue(self, itemIssueSerializer):

        if itemIssueSerializer.is_valid():

            object = itemIssueSerializer.save()

            return JsonResponse({

                'status': True,
                'message': "Item issued",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'status': False,
                    'message': itemIssueSerializer.errors

                })

    def create(self, request, *args, **kwargs):

        itemIssueSerializer = self.get_serializer(data = {

            'item': request.GET['item'],
            'issuedToUser': request.GET['issuedToUser'],
            'returnDate': request.GET['returnDate']

        })

        return self.createIssue(itemIssueSerializer)
