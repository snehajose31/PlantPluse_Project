from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def registration(request):
    return render(request,'registration.html')
def about(request):
    return render(request,'about.html')