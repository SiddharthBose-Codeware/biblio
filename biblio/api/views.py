from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializers import *
from api.modelfunctions import *
from rest_framework.permissions import AllowAny, IsAuthenticated

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

class AddLibraryItemType(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        pass
