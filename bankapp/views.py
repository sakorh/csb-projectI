from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, password_validation, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Account
import sqlite3

#fix to flaw 1
#@login_required
def homePageView(request, username):

    accounts = Account.objects.exclude(username=username)
    balance = Account.objects.get(username=username)
    return render(request, 'index.html', {'accounts': accounts, 'user':username, 'balance': balance.balance})
    
    """if not request.user.username == username:
        return HttpResponse(status=403)
    accounts = Account.objects.exclude(user=User.objects.get(pk=request.user.id))
    balance = Account.objects.get(user=User.objects.get(username=username))
    return render(request, 'index.html', {'accounts': accounts, 'user':username, 'balance': balance.balance})"""

def transferView(request, username):

    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        to = Account.objects.get(username=request.POST.get('to'))
        user = Account.objects.get(username=username)

        user.balance -= amount
        to.balance += amount

        user.save()
        to.save()
	
    return HttpResponseRedirect(reverse('bankapp:home', args=(username,)))

def loginView(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        #comment out lines 48-52 to fix flaw 2
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        sql = 'SELECT username FROM bankapp_account WHERE username ="' + username + '" AND password ="' + password + '"'
        user = cursor.execute(sql).fetchone()
        
        #fix to flaw 2
        #user = authenticate(request, username=username, password=password)
        
        if user:
            request.session['user'] = user[0] #comment this out to fix flaw 2
            #login(request, user)
            return HttpResponseRedirect(reverse('bankapp:home', args=(user[0],)))
            #return HttpResponseRedirect(reverse('bankapp:home', args=(username,)))
        
    return render(request, 'login.html')

def logoutView(request, username):
    del request.session['user']
    #logout(request)
    return HttpResponseRedirect(reverse('bankapp:login'))

def registrationView(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        #comment out lines 78-85 to fix flaw 5
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        sql = f'INSERT INTO bankapp_account (username, password, balance) VALUES ("{username}", "{password}", 0)'
        cursor.execute(sql)
        conn.commit()

        return HttpResponseRedirect(reverse('bankapp:home', args=(username,)))

        #fix to flaw 5
        """try:
            if not password_validation.validate_password(password):

                conn = sqlite3.connect('db.sqlite3')
                cursor = conn.cursor()

                sql = f'INSERT INTO bankapp_account (username, password, balance) VALUES ("{username}", "{password}", 0)'
                cursor.execute(sql)
                conn.commit()

                return HttpResponseRedirect(reverse('bankapp:home', args=(username,)))

        except ValidationError:
            return render(request, 'register.html', {
            'error_message': "Password is too weak. It should be at least 8 characters long and not entirely numeric.",
            })"""
    
    return render(request, 'register.html')


