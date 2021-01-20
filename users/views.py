from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser
from .forms import CustomUserCreationForm

def register(request):
    print(request.method)    
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        print('form errors : ' + str(form.errors))
        
        if form.is_valid():
            form.save()
            messages.success(request, ("User has been added"))
            return redirect('users:index')
        else:
            messages.success(request, (form.errors))
            return redirect('users:index')#, context)

    form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/index.html', context)

def index(request):
    form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/index.html', context)

def signin(request):
    context = {}

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print('form is valid')
            user = form.get_user()
            login(request, user)

            currentUser = CustomUser.objects.filter(email=request.POST.get('username'))
            request.session['name'] = currentUser[0].name
            request.session['email'] = currentUser[0].email
            request.session['userId'] = currentUser[0].id
            return redirect('users:index')
        else:
            return render(request, 'users/index.html', context)    
    else:
        return render(request, 'users/index.html', context)