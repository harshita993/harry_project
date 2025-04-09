from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from my_app.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

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
            return redirect('login')
                 
    return render(request,'login.html')
@login_required(login_url='login')
def index(request):

    variable = {
        'instutue_name':"sutex bank"
        
    }
    if request.user.is_authenticated:
        messages.success(request, f"Welcome, {request.user.username}!")
    return render(request,"index.html",variable)
@login_required(login_url='login')
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

@login_required(login_url='login')
def about(request):   
    return render(request,"about.html")
@login_required(login_url='login')
def service(request):   
    return render(request,"service.html")
@login_required(login_url='login')
def update_contact(request,id):
    contact = Contact.objects.get(id=id)   
    if request.method == "POST":
        
        contact.name = request.POST.get("name")
        contact.phone = request.POST.get("phone")
        contact.email = request.POST.get("email")
        contact.desc = request.POST.get("desc")
        contact.date = datetime.today()
        contact.save()
        messages.success(request, f"{contact.name}'s info was updated successfully.")
        return redirect('contact')

    return render(request, "update_contact.html", {'contact': contact})
@login_required(login_url='login')
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    messages.success(request, f"{contact.name}'s record was deleted successfully.")
    return redirect('contact')
def logoutuser(request):
    logout(request)
    return redirect("login")
