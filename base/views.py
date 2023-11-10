from arrow import get
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm


def home(request):
    rooms=Room.objects.all()
    topics=Topic.objects.all()
    context={'rooms':rooms, 'topics':topics}
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