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
from django.urls import path, include
from api.views import *
from biblio.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()

router.register('subject_types', LibrarySubjectTypeView, base_name = 'subject_types')
router.register('authors', LibraryAuthorView, base_name = 'authors')
router.register('item_types', LibraryItemTypeView, base_name = 'item_types')
router.register('item_types_book', LibraryBookItemTypeView, base_name = 'item_types_book')
router.register('issue_item', LibraryItemIssueView, base_name = 'issue_item')
router.register('items', LibraryItemView, base_name = 'items')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/create_user', CreateUserAccountAPIView.as_view()),
    path('api/auth/create_admin', CreateAdminAccountAPIView.as_view()),
    path('api/auth/login_user', LoginUserAPIView.as_view()),
    path('api/auth/login_admin', LoginAdminAPIView.as_view()),
    #path('api/subject_types/get', LibrarySubjectTypeView.as_view()),
    path('api/', include(router.urls)),
    path('api/auth/update_account_details', UpdateAccountAPIView.as_view()),
    path('api/auth/token', TokenObtainPairView.as_view()),
    path('api/auth/refresh_token', TokenRefreshView.as_view())

    # path('api/', APIView.as_view())
]
