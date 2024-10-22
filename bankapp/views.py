from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Account
import sqlite3

def homePageView(request):

    if request.session.get('user'):
        username = request.session.get('user') 
        #username = User.objects.get(username=request.session.get('user'))
        accounts = Account.objects.exclude(username=request.session.get('user'))
        balance = Account.objects.get(username=request.session.get('user'))
        #accounts = Account.objects.exclude(user=User.objects.get(username=request.session.get('user')))
        #balance = Account.objects.get(user=User.objects.get(username=request.session.get('user')))
        return render(request, 'index.html', {'accounts': accounts, 'user':username, 'balance': balance.balance})
    return render(request, 'login.html')


def transferView(request):

    #fix to flaw 1
    """if request.method == "POST":
        amount = int(request.POST.get('amount'))
        to = Account.objects.get(username=request.POST.get('to'))
        user = Account.objects.get(username=request.session.get('user'))

        user.balance -= amount
        to.balance += amount

        user.save()
        to.save()"""
    amount = int(request.GET.get('amount'))
    to = Account.objects.get(username=request.GET.get('to'))
    user = Account.objects.get(username=request.session.get('user'))

    user.balance -= amount
    to.balance += amount

    user.save()
    to.save()
	
    return redirect('/')

def loginView(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        #comment out lines 56-60 to fix flaw 2
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        sql = 'SELECT username FROM bankapp_account WHERE username ="' + username + '" AND password ="' + password + '"'
        user = cursor.execute(sql).fetchone()
        
        #fix to flaw 2
        #user = authenticate(request, username=username, password=password)
        
        if user:
            request.session['user'] = user[0] #comment this out to fix flaw 2
            #request.session['user'] = username
            return HttpResponseRedirect(reverse('bankapp:home'))
        
    
    
    return redirect('/')

def logoutView(request):
    del request.session['user']
    return HttpResponseRedirect(reverse('bankapp:home'))

def registrationView(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        #comment out lines 86-93 to fix flaw 5
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        sql = f'INSERT INTO bankapp_account (username, password, balance) VALUES ("{username}", "{password}", 0)'
        cursor.execute(sql)
        conn.commit()

        return HttpResponseRedirect(reverse('bankapp:home'))

        #fix to flaw 5
        """try:
            if not password_validation.validate_password(password):

                conn = sqlite3.connect('db.sqlite3')
                cursor = conn.cursor()

                sql = f'INSERT INTO bankapp_account (username, password, balance) VALUES ("{username}", "{password}", 0)'
                cursor.execute(sql)
                conn.commit()

                return HttpResponseRedirect(reverse('bankapp:home'))

        except ValidationError:
            return render(request, 'register.html', {
            'error_message': "Password is too weak. It should be at least 8 characters long and not entirely numeric.",
            })"""
    
    return render(request, 'register.html')


