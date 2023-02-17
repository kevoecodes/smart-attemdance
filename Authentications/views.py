from django.shortcuts import render, redirect
from django.http import request, QueryDict
from bson import json_util, ObjectId
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response

def Login_View(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login-page')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login-page')
    
    if request.method == "GET":
        return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('login-page')
