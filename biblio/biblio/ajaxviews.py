from django.shortcuts import render
from django.http import HttpResponse

class AJAXViews:

    def getManageLibraryItems(request):

        return render(request, "ajaxhtml/libraryitemsworkarea.html", {})

    def getManageSubjectItems(request):

        return render(request, "ajaxhtml/subjecttypesworkarea.html", {})

    def getManageItemItems(request):

        return render(request, "ajaxhtml/itemtypesworkarea.html", {})

    def getManageAuthors(request):

        return render(request, "ajaxhtml/authorworkarea.html", {})

    def getManageIssueItems(request):

        return render(request, "ajaxhtml/issueitemsworkarea.html", {})
