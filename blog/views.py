
from django.shortcuts import render, redirect
#from .models import Product, Customer, OrderItem, Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render
from django.http import HttpResponse
import os.path
from .models import FilesAdmin

# Create your views here.

def index(request):
    context = {
        #'products': products,
        "title": "Home",
    }

    return render(request, 'blog/home.html', context)

def say_hello(request):
    return HttpResponse('Hello World')

def home(request):
    context={'file':FilesAdmin.objects.all()}
    return render(request, 'blog/home.html', context)

def download(request, path):
    file_path=os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response=HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response


    raise Http404



def registerPage(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmation')

        if User.objects.filter(email=email_address).exists():
            messages.error(request, "the email is Already taken")
            return redirect('register')

        elif password1 != password2:
            messages.warning(request, "Your Password Does not match.")
            return redirect('register')

        user1 = User.objects.create_user(username=username, email=email_address, password=password1)
        user1.save()
        messages.success(request, 'You have successfully Registered')
        return redirect('login')


    context = {
      'title': 'register',
    }
    return render(request, 'blog/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')

        user1 = authenticate(username=username, password=password1)
        if user1 is not None:
            login(request, user1)
            return redirect('home')

        else:
            messages.info(request, "invalid Credentials")
            return redirect('login')

    context = {
        'title': 'login'
    }
    return render(request, 'blog/login.html', context)


def logoutPage(request):
    logout(request)
    context = {
        'title': 'Logout'
    }
    return render(request, 'blog/logout.html',context)
