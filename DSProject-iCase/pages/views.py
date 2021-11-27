from django.shortcuts import render

# Create your views here.

def home_view(request,*args,**kwargs):
    return render(request,"main.html",{})

def cases_view(request,*args,**kwargs):
    return render(request,"cases.html",{})

def collection_view(request,*args,**kwargs):
    return render(request,"collection.html",{})