from django.shortcuts import render,HttpResponse

def index(request):
    variable = {
        'instutue_name':"sutex bank"
        
    }
    return render(request,"index.html",variable)
def contact(request):
    return render(request,"contact.html")
def about(request):   
    return render(request,"about.html")
def service(request):   
    return render(request,"service.html")
