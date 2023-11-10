from arrow import get
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm


def home(request):
    rooms=Room.objects.all()
    return render(request,'base/home.html',{'rooms':rooms})

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