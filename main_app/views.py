from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import contact
# from django.http import HttpResponse
def home(request):
    context={}
    if request.user.is_authenticated:
        context['loged_in']=True
        return render(request,'home.html',context)
    return render(request,'home.html')
def summary(request):
    if request.user.is_authenticated:
       return render(request,'summary.html')
    else:
       messages.error(request,'please login first !')
       return redirect('log_reg')
        
def log_reg(request):
    # login validation
    context={}
    if request.method=="POST":
        if request.POST.get('form_type')=='login_type':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                # messages.success(request,'login successfull')
                return redirect('home')
            else:
                messages.error(request,'Invalid username or password !')

        elif request.POST.get('form_type')=='register_type':
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')

            if not username or not email or not password:
                messages.error(request,'please fill all fields !')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'username already exists !')
                context['form_type']='register_type'
                return render(request,'log_reg.html',context)
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request,'Account successfully created !')
                return redirect('log_reg')

    return render(request,'log_reg.html')

def logout_view(request):
    logout(request)
    messages.success(request,'successfully Logout ! Please Login')
    return redirect('log_reg')
# Create your views here.
#contact
def contact_us(request):
    context={}
    if request.method=="POST":
      if request.user.is_authenticated:
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        country=request.POST.get('country')
        subject=request.POST.get('subject')
        if not firstname or not lastname or not country or not subject:
            messages.error(request,'please enter all fields')
            context['field_missing']='missing'
            return render(request,'home.html',context)
        else:
            cont=contact.objects.create(first_name=firstname, last_name=lastname, country=country, subject=subject)
            cont.save()
            messages.success(request,"Message have been send ,Thank You !")
            return redirect('home')
      else:
        messages.error(request,'please logiin first')
        return redirect('log_reg')
    return render(request,'home.html')