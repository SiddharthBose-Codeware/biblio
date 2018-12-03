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
from biblio.ajaxviews import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.authtoken import views as rest_framework_views

def handler404(request, exception, template_name = "404.html"):
    pass




router = routers.DefaultRouter()

router.register('subject_types', LibrarySubjectTypeView, base_name = 'subject_types')
router.register('authors', LibraryAuthorView, base_name = 'authors')
router.register('item_types', LibraryItemTypeView, base_name = 'item_types')
router.register('item_types_book', LibraryBookItemTypeView, base_name = 'item_types_book')
router.register('item_issues', LibraryItemIssueView, base_name = 'issue_item')
router.register('items', LibraryItemView, base_name = 'items')
router.register('libraries', LibraryView, base_name = 'libraries')
router.register('get_library_members', GetLibraryMembersView, base_name = 'get_library_members')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/create_user', CreateUserAccountAPIView.as_view()),
    path('api/auth/create_admin', CreateAdminAccountAPIView.as_view()),
    path('api/auth/login_user', local_views.get_auth_token.as_view()),
    path('api/auth/logout_user', local_views.logout_user.as_view()),
    path('api/auth/login_admin', LoginAdminAPIView.as_view()),
    path('api/', include(router.urls)),
    path('api/auth/update_account_details', UpdateAccountAPIView.as_view()),
    # path('api/auth/token', TokenObtainPairView.as_view()),
    # path('api/auth/refresh_token', TokenRefreshView.as_view()),
    # path('api/auth/verify_token', TokenVerifyView.as_view()),
    path('api/get_library_name', GetLibraryNameView.as_view()),
    path('', Views.getIndexPage),
    path('admin-dashboard', Views.getAdminDashboard),
    path('user-dashboard', Views.getUserDashboard),
    path('login', Views.getLogin),
    path('signup', Views.getSignup),

    path('ajaxHTML/manageLibraryItems', AJAXViews.getManageLibraryItems),
    path('ajaxHTML/manageSubjectTypes', AJAXViews.getManageSubjectItems),
    path('ajaxHTML/manageItemTypes', AJAXViews.getManageItemItems),
    path('ajaxHTML/manageAuthors', AJAXViews.getManageAuthors),
    path('ajaxHTML/manageIssueItems', AJAXViews.getManageIssueItems),

]

urlpatterns += staticfiles_urlpatterns()
