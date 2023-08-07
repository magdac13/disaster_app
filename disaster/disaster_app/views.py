from django.views import View
from django.shortcuts import HttpResponse, redirect, render
from .models import Asteroid, NaturalEvent
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import os



class GetDataAndSaveToDBView(View):
    """ Fetches data from API and saves it to database. """

    def get(self, request):
        asteroid_manager = Asteroid.objects
        natural_events_manager = NaturalEvent.objects

        # Pobierz dane z API NASA
        asteroid_data = asteroid_manager.get_data_from_api()
        natural_events_data = natural_events_manager.get_data_from_api()

        # Zapisz dane do bazy danych
        asteroid_manager.save_data_to_db(asteroid_data)
        natural_events_manager.save_data_to_db(natural_events_data)

        return HttpResponse("Dane zostały pobrane i zapisane do bazy danych.")
    

class MainView(View):
    def get(self, request):
        return render(request, 'main_page.html')
    
    
class LoginUser(View):
    
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):    
        
        username = request.POST.get['username']
        password = request.POST.get['password']
            
            # Authenticate 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging you in.')
            return redirect('login')
            
        
        


class LogoutUser(View):
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')
    
    
    