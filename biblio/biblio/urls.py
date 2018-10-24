"""biblio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import *
from biblio.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/create_user', CreateUserAccountAPIView.as_view()),
    path('api/auth/create_admin', CreateAdminAccountAPIView.as_view()),
    path('api/auth/login_user', LoginUserAPIView.as_view()),
    path('api/auth/login_admin', LoginAdminAPIView.as_view()),
    path('api/auth/update_account_details', UpdateAccountAPIView.as_view()),
    path('api/auth/token', TokenObtainPairView.as_view()),
    path('api/auth/refresh_token', TokenRefreshView.as_view())

    # path('api/', APIView.as_view())
]
