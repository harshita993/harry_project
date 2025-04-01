from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from my_app.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
                 
    return render(request,'login.html')
def index(request):

    variable = {
        'instutue_name':"sutex bank"
        
    }
    if request.user.is_authenticated:
        messages.success(request, f"Welcome, {request.user.username}!")
    return render(request,"index.html",variable)
def contact(request):
    if request.method == "POST":
        firstname = request.POST.get("name")
        phoneno = request.POST.get("phone")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        date = datetime.today()
        contact = Contact(name = firstname,phone=phoneno,email=email,desc=desc,date=date)
        contact.save()
        messages.success(request,f"{contact.name} was successfully inserted")
        
        
        print(f"Received Contact Form: {firstname}, {phoneno}, {email}, {desc}")  
        return redirect("contact")  
    contacts = Contact.objects.all()
    return render(request, "contact.html",{'contacts':contacts})
def about(request):   
    return render(request,"about.html")
def service(request):   
    return render(request,"service.html")
def logoutuser(request):
    logout(request)
    return redirect("login")
