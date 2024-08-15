from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .models import Todo
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            todo = request.POST.get('todo')
            if Todo.objects.filter(user=request.user, name=todo):
                messages.info(request ,'Todo already exists.')
                return redirect('home')
            new_todo = Todo(user=request.user, name=todo)
            new_todo.save()

        all_todos = Todo.objects.filter(user=request.user)
    else:
        all_todos = []  

    context = {
        'all_todos': all_todos,
        'username': request.user
    }

    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.info(request ,'User already exists. You can login!')
            return redirect('login')
        
        if len(password) < 3:
            messages.info(request , 'Length of password should be at least 3.')
            return redirect('register')
        new_user = User.objects.create_user(username=username , email=email , password=password)
        new_user.save()
        messages.info(request , f'User created successfully. You can login now')
        return redirect('login')
    return render(request , 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        
        valid_user  = auth.authenticate(username=username , password=password)

        if valid_user is not None:
            auth.login(request, valid_user)
            return redirect('home')
        else:
            messages.info(request , "Username and password didn't matched")
            return redirect('login')

    return render(request, 'login.html')


def delete(request, name):
    get_todo = Todo.objects.get(user=request.user, name=name)
    get_todo.delete()
    messages.info(request , f'Todo: {name} deleted successfully.')

    return redirect('home')


def update(request, name):
    get_todo = Todo.objects.get(user=request.user, name=name)
    get_todo.status = True
    get_todo.save()
    messages.info(request , f'Todo: {name} completed successfully.')
    return redirect('home')


def unupdate(request, name):
    get_todo = Todo.objects.get(user=request.user, name=name)
    get_todo.status = False
    get_todo.save()
    return redirect('home')


def toggle_status(request, name):
    get_todo = Todo.objects.get(user=request.user, name=name)
    get_todo.status = not get_todo.status  
    get_todo.save()

    status_message = 'completed sucessfully' if get_todo.status else 'marked as incomplete'
    messages.info(request, f'Todo: {name} {status_message}.')
    
    return redirect('home')



def update_todo(request, name):
    todo = get_object_or_404(Todo, user=request.user, name=name)

    if request.method == 'POST':
        updated_name = request.POST.get('todo')
        
        if Todo.objects.filter(user=request.user, name=updated_name).exists():
            messages.info(request, 'Todo with this name already exists.')
            return redirect('update_todo', name=name)
        
        todo.name = updated_name
        todo.save()

        messages.info(request, f'Todo updated successfully to: {updated_name}.')
        return redirect('home')

    context = {
        'todo': todo
    }

    return render(request, 'update_todo.html', context)




def logout(request):
    auth.logout(request)
    return redirect('login')