from django.urls import paths
from views import *

urlpatterns = [

    path("api/auth/create_user", CreateUserAccountAPIView.as_view())

]
