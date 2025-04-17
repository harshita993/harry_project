from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from datetime import datetime
from my_app.models import Contact, Icecream,CartItem, OrderItem, Order
from blog.models import BlogPost
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import IcecreamForm
from django.core.paginator import Paginator


def get_categories():
    return Icecream.objects.values_list('category', flat=True).distinct()
def register_view(request):
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        make_superuser = 'is_superuser' in request.POST

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        if make_superuser:
            user.is_superuser = True
            user.is_staff = True 
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
@login_required(login_url='login')
def index(request):
    categories = get_categories()
    icecream_list = Icecream.objects.all()
    paginator = Paginator(icecream_list, 3) 
    page_number = request.GET.get('page')
    icecreams = paginator.get_page(page_number)
    if request.user.is_authenticated:
        messages.success(request, f"Welcome, {request.user.username}!")
    return render(request,"index.html",{'icecreams': icecreams,'categories': categories})

@login_required(login_url='login')
def contact(request):
    categories = get_categories()
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
    return render(request, "contact.html",{'contacts':contacts, 'categories': categories})

@login_required(login_url='login')
def about(request): 
    categories = get_categories()
    admin_users = User.objects.filter(is_superuser=True) 
    print("Admins:", admin_users)
    return render(request,"about.html", {'admin_users': admin_users,'categories': categories})
@login_required(login_url='login')
def service(request):   
    categories = get_categories()
    return render(request,"service.html",{'categories': categories})
def services_by_category(request, category):
    items = Icecream.objects.filter(category=category)
    categories = Icecream.objects.values_list('category', flat=True).distinct()
    return render(request, 'category_service.html', {
        'icecreams': items,
        'categories': categories,
        'selected_category': category
    })

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
@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect("login")
@login_required
def add_icecream(request):
    categories = get_categories()
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
    return render(request, 'add_icecream.html', {'form': form, 'categories': categories})
@login_required(login_url='login')
def icecream_detail(request, id):
    icecream = get_object_or_404(Icecream, id=id)
    return render(request, 'icecream_detail.html', {'icecream': icecream})
@login_required(login_url='login')
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
            return redirect('home')
    else:
        form = IcecreamForm(instance=icecream)
    return render(request, 'icecream_edit.html', {'form': form, 'icecream': icecream})
@login_required
def icecream_delete(request, id):
    icecream = get_object_or_404(Icecream, id=id)
    blog_post = BlogPost.objects.filter(icecream=icecream).first() 
    if blog_post:
        blog_post.delete()
    icecream.delete()
    return redirect('home')
@login_required
def add_to_cart(request, icecream_id):
    icecream = Icecream.objects.get(id=icecream_id)
    quantity = int(request.POST.get("quantity", 1))
    cart_item, created = CartItem.objects.get_or_create(user=request.user, icecream=icecream)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f"{icecream.name} added to your cart!")
    return redirect('view_cart')
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.subtotal = item.quantity * item.icecream.price

    total = sum(item.subtotal for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total': total})
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == 'GET':
        total = sum(item.quantity * item.icecream.price for item in cart_items)
        return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

    elif request.method == 'POST':
        address = request.POST.get('address')
        total_amount = sum(item.quantity * item.icecream.price for item in cart_items)

        order = Order.objects.create(user=request.user, total_amount=total_amount, address=address)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                icecream=item.icecream,
                quantity=item.quantity,
                price=item.icecream.price,
                
            )

        cart_items.delete()
        messages.success(request, f"Order placed successfully! Order ID: {order.id}")
        return redirect('home')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('view_cart')
def update_cart_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete() 
        messages.success(request, "Cart updated successfully.")
    return redirect('view_cart')
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  
    
    return render(request, 'order_history.html', {'orders': orders})
@login_required
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('order_history')
    return render(request, 'confirm_delete_order.html', {'order': order})
