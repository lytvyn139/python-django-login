from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')
    
def register(request):
    check = Login.loginObj.user_add(request.POST['first_name'], request.POST['last_name'],request.POST['email'], request.POST['bc1'], request.POST['bc2'])
    print(request.POST) 
    print(check[0])
    if check[0] == True:
        request.session['logged_in'] = check[1].id
        return redirect('/registred')
    else:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')

def registred(request):
    if not 'logged_in' in request.session:
        return redirect('/')
    else:
        check = Login.loginObj.is_logged_in(request.session['logged_in'])
        context = {
            'user': check 
        }
        return render(request,'registred.html',context)

""" LOGIN PART """

def login(request):
    check = Login.loginObj.login_validation(request.POST['email'],request.POST['bc1'])
    if check[0] == True:
        request.session['logged_in'] = check[1]
        return redirect('/success')
    else:
        for message in check[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')

def success(request):
    if not 'logged_in' in request.session:
        return redirect('/')
    else:
        check = Login.loginObj.is_logged_in(request.session['logged_in'])
        context = {
            'user': check 
        }
        return render(request,'success.html',context)
        

