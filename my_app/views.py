from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from datetime import datetime
from my_app.models import Contact, Icecream
from blog.models import BlogPost
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import IcecreamForm
from django.core.paginator import Paginator
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "User registered successfully. You can now login.")
        return redirect('login')

    return render(request, 'register.html')
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

def index(request):
    icecream_list = Icecream.objects.all()
    paginator = Paginator(icecream_list, 3) 
    page_number = request.GET.get('page')
    icecreams = paginator.get_page(page_number)
    if request.user.is_authenticated:
        messages.success(request, f"Welcome, {request.user.username}!")
    return render(request,"index.html",{'icecreams': icecreams})

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
@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect("login")
@login_required
def add_icecream(request):
    if request.method == 'POST':
        form = IcecreamForm(request.POST, request.FILES)
        if form.is_valid():
            icecream = form.save(commit=False)
            icecream.added_by = request.user
            icecream.save()
            
            BlogPost.objects.create(
            title=icecream.name,
            body=icecream.description,
            image=icecream.image,
            author=request.user,
            icecream=icecream
                    )
            return redirect('home')
    else:
        form = IcecreamForm()
    return render(request, 'add_icecream.html', {'form': form})
def icecream_detail(request, id):
    icecream = get_object_or_404(Icecream, id=id)
    return render(request, 'icecream_detail.html', {'icecream': icecream})

def icecream_edit(request, id):
    icecream = get_object_or_404(Icecream, id=id)
    if request.method == 'POST':
        form = IcecreamForm(request.POST, request.FILES, instance=icecream)
        if form.is_valid():
            icecream = form.save(commit=False)
            icecream.save() 

            
            try:
                blog_post = BlogPost.objects.get(icecream=icecream)  
                blog_post.title = icecream.name  
                blog_post.body = icecream.description  
                blog_post.image = icecream.image  
                blog_post.save()  
            except BlogPost.DoesNotExist:
                
                BlogPost.objects.create(
                    title=icecream.name,
                    body=icecream.description,
                    image=icecream.image,
                    author=request.user,
                    icecream=icecream
                )
            return redirect('icecream_detail', id=icecream.id)
    else:
        form = IcecreamForm(instance=icecream)
    return render(request, 'icecream_edit.html', {'form': form, 'icecream': icecream})
@login_required
def icecream_delete(request, id):
    icecream = get_object_or_404(Icecream, id=id)
    blog_post = BlogPost.objects.filter(icecream=icecream).first()  # Using first to get the first match, if any
    if blog_post:
        blog_post.delete()
    icecream.delete()
    return redirect('home')
    