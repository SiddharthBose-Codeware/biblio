from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from django.http import JsonResponse
from api.serializers import *
from api.modelfunctions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters

import json
import urllib

class CreateUserAccountAPIView(APIView):

    def post(self, request):

        validationResult = UserAccountSerializer.validateRequest(request)

        if validationResult != True:

            return JsonResponse({

                'success': False,
                'message': validationResult['message']

            }, status = 201)

        userAccountSerializer = UserAccountSerializer(data = {

            'firstname': request.POST['firstname'],
            'lastname': request.POST['lastname'],
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password']

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

        validationResult = AdminAccountSerializer.validateRequest(request)

        if validationResult != True:

            return JsonResponse({

                'success': False,
                'message': validationResult['message']

            }, status = 201)

        adminAccountSerializer = AdminAccountSerializer(data = {

            'firstname': request.POST['firstname'],
            'lastname': request.POST['lastname'],
            'libraryname': request.POST['libraryname'],
            'email': request.POST['email'],
            'password': request.POST['password']

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

            'email': request.POST['email'],
            'password': request.POST['password'],
            'rememberMe': request.POST['rememberMe']

        }, False)

class LoginAdminAPIView(LoginAPIView):

    def post(self, request):

        return self.login({

            'email': request.POST['email'],
            'password': request.POST['password'],
            'rememberMe': request.POST['rememberMe']

        }, True)

class UpdateAccountAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # toChange = request.POST['toChange']
        #
        # newValue = request.POST['newValue']

        request.user.update(request.POST)

        return JsonResponse({

            'success': True,
            'message': "Account details updated"

        })

class LibrarySubjectTypeView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibrarySubjectTypeSerializer

    filter_backends = (filters.SearchFilter,)

    search_fields = ('type', 'parent__type')

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.subjectTypes.get_queryset().order_by('-id')

    def create(self, request, *args, **kwargs):

        # request.user.library.addSubjectType(request.POST['type'], request.POST['parent'])

        if 'parent' in request.POST:

            subjectTypeSerializer = self.get_serializer(data = {

                'type': request.POST['type'],
                'parent':  request.POST['parent']

            })

        else:

            subjectTypeSerializer = self.get_serializer(data = {

                'type': request.POST['type']

            })


        if subjectTypeSerializer.is_valid():

            object = subjectTypeSerializer.save()

            return JsonResponse({

                'success': True,
                'message': "Created a new subject type.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'success': False,
                    'message': subjectTypeSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibrarySubjectType.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'type': object.type,
            'parent': object.parent

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.POST)

        return JsonResponse({

            'success': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibrarySubjectType.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'success': True,
            'message': "The subject type has been deleted."

        })

    # def create(self, serializer):
    #
    #     help(self)
    #
    #     serializer.save(data = self.request.POST)

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

        return self.request.user.library.authors.get_queryset().order_by('-id')

    def create(self, request, *args, **kwargs):

        authorSerializer = self.get_serializer(data = {

            'name': request.POST['name']

        })

        if authorSerializer.is_valid():

            object = authorSerializer.save()

            return JsonResponse({

                'success': True,
                'message': "Author added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'success': False,
                    'message': subjectTypeSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibraryAuthor.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'name': object.name

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.POST)

        return JsonResponse({

            'success': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryAuthor.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'success': True,
            'message': "The author has been deleted."

        })

class LibraryItemTypeView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibraryItemTypeSerializer

    filter_backends = (filters.SearchFilter,)

    search_fields = ('type',)

    def get_queryset(self):

        # data = self.request.user.library.subjectTypes
        #
        # help(data)
        #
        # serializer = LibrarySubjectTypeSerializer(data, many = True)
        #
        # return Response(serializer.data)

        return self.request.user.library.itemTypes.get_queryset().order_by('-id')

    def createItemType(self, itemTypeSerializer):

        if itemTypeSerializer.is_valid():

            object = itemTypeSerializer.save()

            return JsonResponse({

                'success': True,
                'message': "Item type added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'success': False,
                    'message': subjectTypeSerializer.errors

                })

    def create(self, request, *args, **kwargs):

        itemTypeSerializer = self.get_serializer(data = {

            'type': request.POST['type']

        })

        return self.createItemType(itemTypeSerializer = itemTypeSerializer)

    def partial_update(self, request, *args, **kwargs):

        object = LibraryItemType.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'type': object.type

        }

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.POST)

        return JsonResponse({

            'success': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryItemType.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'success': True,
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

        return self.request.user.library.items.get_queryset().order_by('-id')

    def create(self, request, *args, **kwargs):

        itemSerializer = self.get_serializer(data = {

            'name': request.POST['name'],
            'author': request.POST['author'],
            'itemType': request.POST['itemType'],
            'subjectType': request.POST['subjectType']

        })

        if itemSerializer.is_valid():

            object = itemSerializer.save()

            return JsonResponse({

                'success': True,
                'message': "Item added to library.",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'success': False,
                    'message': itemSerializer.errors

                })

    def partial_update(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        updationData = {

            'name': object.name,
            'subjectType': object.subjectType.pk,
            'itemType': object.itemType.pk,
            'author': object.author.pk

        }

        print("\n\n\n\n" + str(updationData) + "\n\n\n\n")

        updatedObject = self.get_serializer(data = updationData).partial_update(object, request.POST)

        return JsonResponse({

            'success': True,
            'newObjectData': updationData

        })

    def destroy(self, request, *args, **kwargs):

        object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]

        object.delete();

        return JsonResponse({

            'success': True,
            'message': "The item has been deleted."

        })

# class LibraryItemView(viewsets.ModelViewSet):
#
#     permission_classes = (IsAuthenticated,)
#
#     serializer_class = LibraryItemSerializer
#
#     def get_queryset(self):
#
#         # data = self.request.user.library.subjectTypes
#         #
#         # help(data)
#         #
#         # serializer = LibrarySubjectTypeSerializer(data, many = True)
#         #
#         # return Response(serializer.data)
#
#         return self.request.user.library.items.get_queryset().order_by('-id').order_by('-id')
#
#     def get_serializer_class(self):
#
#         if self.request.method == "POST":
#
#             if self.request.POST['itemType'] is None:
#
#                 return LibraryBookItemSerializer
#
#         return LibraryItemSerializer
#
#     # def getLibraryItemSerializer(self, data):
#     #
#     #     if data['itemType'] is None:
#     #
#     #         return self.get_serializer_class(data = {
#     #
#     #             'name': data['name'],
#     #             'author': data['author'],
#     #             'itemType': data['itemType'],
#     #             'subjectType': data['subjectType'],
#     #             'ISBNCode': data['ISBNCode']
#     #
#     #         })
#     #
#     #     itemSerializer = self.get_serializer_class(data = {
#     #
#     #         'name': data['name'],
#     #         'author': data['author'],
#     #         'itemType': data['itemType'],
#     #         'subjectType': data['subjectType']
#     #
#     #     })
#
#     def createItem(self, itemSerializer):
#
#         if itemSerializer.is_valid():
#
#             object = itemSerializer.save()
#
#             return JsonResponse({
#
#                 'success': True,
#                 'message': "Item added to library.",
#                 'id': object.pk
#
#             })
#
#         else:
#
#                 return JsonResponse({
#
#                     'success': False,
#                     'message': itemSerializer.errors
#
#                 })
#
#     def create(self, request, *args, **kwargs):
#
#         itemSerializer = None
#
#         if request.POST['itemType'] is None:
#
#             itemSerializer = self.get_serializer(data = {
#
#                 'name': request.POST['name'],
#                 'author': request.POST['author'],
#                 'itemType': request.POST['itemType'],
#                 'subjectType': request.POST['subjectType'],
#                 'ISBNCode': request.POST['ISBNCode']
#
#             })
#
#         else:
#
#             itemSerializer = self.get_serializer(data = {
#
#                 'name': request.POST['name'],
#                 'author': request.POST['author'],
#                 'itemType': request.POST['itemType'],
#                 'subjectType': request.POST['subjectType']
#
#             })
#
#         # help(itemSerializer)
#
#         return self.createItem(itemSerializer)
#
#     def partial_update(self, request, *args, **kwargs):
#
#         object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]
#
#         updationData = {
#
#             'name': object.name,
#             'subjectType': object.itemType,
#             'itemType': object.itemType,
#             'type': object.itemType,
#             'author': object.author
#
#         }
#
#         print(updationData)
#
#         updatedObject = self.get_serializer(data = updationData).partial_update(object, request.POST)
#
#         return JsonResponse({
#
#             'success': True,
#             'newObjectData': updationData
#
#         })
#
#     def destroy(self, request, *args, **kwargs):
#
#         object = LibraryItem.objects.filter(pk = kwargs['pk'])[0]
#
#         object.delete();
#
#         return JsonResponse({
#
#             'success': True,
#             'message': "The item has been deleted."
#
#         })

class LibraryBookItemView(LibraryItemView):

    serializer_class = LibraryBookItemSerializer

    def get_queryset(self):

        return self.request.user.library.itemTypes.filter(type = None)

    def create(self, request, *args, **kwargs):

        bookItemSerializer = self.get_serializer(data = {

            'name': request.POST['name'],
            'author': request.POST['author'],
            'itemType': request.POST['itemType'],
            'subjectType': request.POST['subjectType'],
            'ISBNCode': request.POST['ISBNCode']

        })

        return self.createItem(bookItemSerializer)


class LibraryItemIssueView(viewsets.ModelViewSet):

    serializer_class = LibraryItemIssueSerializer

    def get_queryset(self):

        return self.request.user.library.issues.get_queryset().order_by('-id')

    def createIssue(self, itemIssueSerializer):

        if itemIssueSerializer.is_valid():

            object = itemIssueSerializer.save()

            return JsonResponse({

                'success': True,
                'message': "Item issued",
                'id': object.pk

            })

        else:

                return JsonResponse({

                    'success': False,
                    'message': itemIssueSerializer.errors

                })

    def create(self, request, *args, **kwargs):

        itemIssueSerializer = self.get_serializer(data = {

            'item': request.POST['item'],
            'issuedToUser': request.POST['issuedToUser'],
            'returnDate': request.POST['returnDate']

        })

        return self.createIssue(itemIssueSerializer)

class AddUserToLibraryView(APIView):

    def post(self, request):

        user = Account.objects.filter(request.POST['userId'])

        request.user.library.addUser({

            "user": user

        })

        return JsonResponse({

            'success': True,
            'message': "User added to the library."

        })

class GetLibraryNameView(APIView):

    def get(self, request):

        if request.user:

            return JsonResponse({

                'libraryName': request.user.library.name

            })

class GetLibraryNameView(APIView):

    def get(self, request):

        if request.user:

            return JsonResponse({

                'libraryName': request.user.library.name

            })

class GetLibraryMembersView(viewsets.ModelViewSet):

    serializer_class = UserAccountModelSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.SearchFilter,)

    search_fields = ('name', 'username', 'email')

    def get_queryset(self):

        return self.request.user.library.users.get_queryset()

    def get(self, request):

        if request.user:

            return JsonResponse(json.dumps(list(request.user.library.users)))


class LibraryView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    serializer_class = LibrarySerializer

    filter_backends = (filters.SearchFilter,)

    search_fields = ('name',)

    def get_queryset(self):

        return Library.objects.all()
