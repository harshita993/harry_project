from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from my_app.models import Contact
from django.contrib import messages
def index(request):
    variable = {
        'instutue_name':"sutex bank"
        
    }
    messages.success(request,"message have ben sent")
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
