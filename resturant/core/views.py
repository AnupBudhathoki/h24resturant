from django.shortcuts import render, redirect
from .models import Customer, Category, Momo
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import qrcode # type: ignore


# Create your views here.

def save(request):
    
    return render(request, 'core/index.html')

def index(request):
    category=Category.objects.all()

    catid=request.GET.get('category')
    if catid:
        momo=Momo.objects.filter(category=catid)
    else:
        momo=Momo.objects.all()

    context={
        "category":category,
        "momo":momo,
        "date":datetime.now
    }



    if request.method == "POST":
        data=request.POST

        name=data['name']
        email=data['email']
        number=data['phone']
        message=data['message']

        
        cus=Customer(name=name, number=number, email=email, message=message, )
        cus.save()

        messages.success(request, f"{name} your form is submitted !!!")
        return redirect('index')

    return render(request, 'core/index.html', context)


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')


def services(request):
    return render(request, 'core/services.html')


@login_required(login_url='log_in')
def menu(request):
    qr=qrcode.QRCode(version=1,box_size=40,border=2)
    qr.add_data("https://www.google.com")
    qr.make(fit=True)
    q=qr.make_image(fill_color="red",back_color="yellow")
    q.save("core/static/images/anup.png")
    return render(request, 'core/menu.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def base(request):
    return render(request, 'base.html')

def log_in(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        remember_me=request.POST.get("remember_me")


        if not User.objects.filter(username=username).exists():
            messages.error(request, "username not available")
            return redirect('log_in')

        data=authenticate(username=username, password=password)

        if data is not None:
            login(request, data)

            if remember_me:
                request.session.set_expiry(120000000)

            else:
                request.session.set_expiry(0)

            next=request.POST.get("next","")
            return redirect(next if next else 'index')
        else:
            messages.error(request, "password is not correct")

            return redirect('log_in')

    next=request.GET.get("next","")
    return render(request, 'accounts/log_in.html',{'next':next})

def log_out(request):
    logout(request)
    return redirect('log_in')

def register(request):
    if request.method=='POST':
        fname=request.POST['fullname']
        uname=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['confirm_password']

        if password==password1:
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exits")
                return redirect('register')
            
            if User.objects.filter(username=uname).exists():
                messages.error(request,"username already exits")
                return redirect('register')
            error=[]
            if not re.search(r"[A-Z]",password):
                error.append("password must caontain at least a capital word")
                
            
            if not re.search(r"\d",password):
                error.append("password must caontain at least a number")
        
           
            try:
                validate_password(password)
                if not error:
                    User.objects.create_user(first_name=fname, username=uname, email=email,password=password)
                    return redirect('index')

                
            except ValidationError as e:
                for j in error:
                        messages.error(request,j)
                for i in e.messages:
                    messages.error(request,i)

                return redirect('register')
        else:
            messages.error(request, "Your passwords dont match")
            return redirect('register')
    return render(request, 'accounts/register.html')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method== 'POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("log_in")
    return render(request, 'accounts/change_password.html',{'form':form})