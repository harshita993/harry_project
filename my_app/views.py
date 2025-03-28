from django.shortcuts import render,HttpResponse,redirect

def index(request):
    variable = {
        'instutue_name':"sutex bank"
        
    }
    return render(request,"index.html",variable)
def contact(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        phoneno = request.POST.get("phoneno")
        email = request.POST.get("email")
        desc = request.POST.get("desc")

        print(f"Received Contact Form: {firstname}, {phoneno}, {email}, {desc}")  # Debugging

        return redirect("contact")  

    return render(request, "contact.html")
def about(request):   
    return render(request,"about.html")
def service(request):   
    return render(request,"service.html")
