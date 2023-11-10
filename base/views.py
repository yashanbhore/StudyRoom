from arrow import get
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic,User
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages

def loginPage(request):
    

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try: 
            user = User.objects.get(email=email )
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        
    context = {}
    return render(request, 'base/login_register.html', context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
            )
    room_count = rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms, 'topics':topics,'room_count': room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    rooms=Room.objects.get(id=pk)
    return render(request,'base/room.html',{'rooms':rooms})

def createRoom(request):       
    form=RoomForm()     
    if request.method == 'POST':
       form=RoomForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here.') 
    
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form': form}
    return render(request,'base/room_form.html',context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!') 

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})