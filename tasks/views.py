from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required(login_url='/login/')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('-id')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, user=request.user)
            return redirect('home')
    return render(request, 'tasks/home.html', {'tasks': tasks})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('home')

def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')

def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
            return redirect('home')
    return render(request, 'tasks/edit.html', {'task': task})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tasks/signup.html', {'error': 'Username already taken'})
    return render(request, 'tasks/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tasks/login.html', {'error': 'Invalid login'})
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')