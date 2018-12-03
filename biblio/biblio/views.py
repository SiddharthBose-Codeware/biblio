from django.shortcuts import render
from django.http import HttpResponse

from biblio.models import UserAccount, AdminAccount, Account

class Views:

    def getIndexPage(request):

        return render(request, "index.html", {})

    def getAdminDashboard(request):

        return render(request, "final-dashboard.html", {})

    def getUserDashboard(request):

        return render(request, "user-dashboard.html", {})

    def getLogin(request):

        return render(request, "login.html", {})

    def getSignup(request):

        return render(request, "signup.html", {})
