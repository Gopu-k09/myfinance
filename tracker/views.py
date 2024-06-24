from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Entry
from .forms import EntryForm, UserRegistrationForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    entries = Entry.objects.filter(user=request.user)
    return render(request, 'tracker/dashboard.html', {'entries': entries})

def add_entry(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = EntryForm()
    return render(request, 'tracker/add_entry.html', {'form': form})

def summary(request):
    if not request.user.is_authenticated:
        return redirect('login')
    entries = Entry.objects.filter(user=request.user)
    total_income = sum(entry.amount for entry in entries if not entry.is_expense)
    total_expense = sum(entry.amount for entry in entries if entry.is_expense)
    return render(request, 'tracker/summary.html', {'total_income': total_income, 'total_expense': total_expense})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tracker/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
