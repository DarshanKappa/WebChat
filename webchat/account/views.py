from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from chat.views import friend_list


# Create your views here.


def account(request):

    if request.method == "POST":
        
        firstname = request.POST.get('first_name','')
        lastname = request.POST.get('last_name','')
        number = request.POST.get('number','')
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')

        print(firstname)
        print(lastname)
        print(number)
        print(password1)
        print(password2)

        if password1 == password2:

            if User.objects.filter(username=number).exists():
                messages.info(request,'mobile number taken')
                return redirect('account')
            else:
                
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=number,password=password1)
                user.save()

                return HttpResponse('<h2 style="margin:5vw">Registration Succesfully</h2>')

        
        else:
            messages.info(request,'Confirm password not match')
            return redirect('account')



    return render(request,'register.html')


def login(request):

    if request.method == "POST":
        
        number = request.POST.get('number','')
        password = request.POST.get('password','')

        print(number)
        print(password)

        user = auth.authenticate(username=number,password=password)
        if user is not None:
            auth.login(request, user)
            print("........login.........")
            messages.info(request,'Login')
            return redirect('friend_list')
            
        else:
            messages.info(request,'Number or Password is wrong')
            return redirect('login')
            

    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')