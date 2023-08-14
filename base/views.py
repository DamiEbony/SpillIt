from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import FormRoom, UserForm, MyUserForm


def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Please provide both username and password.")
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User does not exist!")
            else:
                user = authenticate(request,email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid email or password.")
            
    context = {'page': page}
    return render(request, 'base/login.html', context)


def logoutView(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserForm()
    
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration Error Occurred')
    context = {'form': form}
    return render(request, 'base/login.html', context)
    
    
   

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms  = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
                                 )
    
    room_count = rooms.count()
    topic = Topic.objects.all()[0:3]
    user = User.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context = {'rooms': rooms, 'topic': topic, 
               'room_count': room_count,
               'room_messages': room_messages,
               'user': user}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    
   
    guests = room.guests.all()
    if request.method == 'POST':
        messager = Message.objects.create(
            user=request.user, 
            room=room, 
            body=request.POST.get('body'))
        room.guests.add(request.user)
        
        return redirect('room', pk=room.id)
    context = {'room': room, 
               'room_messages': room_messages, 
               'guests': guests, 
               'obj': room.name,
               'obj_type': 'room',
              
              }
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 
               'room_messages': room_messages,
               'topic': topic}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createRoom(request):
    form = FormRoom()
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
            
        )
        return redirect('home')
            
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/form_room.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = FormRoom(instance=room)
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context ={'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/form_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
     
    if request.user != room.host:
        return HttpResponse('Access Denied, You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    user_message = get_object_or_404(Message, id=pk, user=request.user)
    room_id = user_message.room_id 
    if request.method == 'POST':
        user_message.delete()
        return redirect('room', pk=room_id)
    
    context = {'obj': user_message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
            
        
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)
    
    
    context = {'topic': topic}
    return render(request, 'base/topics.html', context)

def latestPage(request):
    room_messages = Message.objects.all()
    
    context = {'room_messages': room_messages}
    return render(request, 'base/latest.html', context)
    
        
    
    
           
        
    