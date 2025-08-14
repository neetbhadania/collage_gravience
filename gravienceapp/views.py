from django.shortcuts import render
from django.http import HttpResponse


def viewdata(request):
    # students = students.objects.all() 
    return render(request,"home.html")                   