from django.shortcuts import render
import requests
from datetime import datetime

from django.contrib.auth import login as auth_login 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomAuthenticationForm
from weather.forms import CustomAuthenticationForm, CustomUserCreationForm


def get_weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        api_key = 'e145ab6af41f4480ab1101636240404' # Replace with your actual API key
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7'
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            
            # Convert dates to day names
            for forecast_day in weather_data['forecast']['forecastday']:
                date_str = forecast_day['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                forecast_day['day_name'] = date_obj.strftime('%A')
            
            
            
            return render(request, 'weather/weather.html', {'weather_data': weather_data})
        else:
            error_message = "Could not retrieve weather data. Please try again."
            return render(request, 'weather/index.html', {'error_message': error_message})
    return render(request, 'weather/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('get_weather') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'weather/signup.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username}")  
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f"User {username} authenticated successfully.")  # Debugging statement
                auth_login(request, user)
                print("Redirecting to get_weather")  # Debugging statement
                return redirect('get_weather')  
            else:
                print("Authentication failed. User not found.") 
        else:
            print("Form is not valid")  # Debugging statement
            print(form.errors)  # Print form errors for debugging
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'weather/login.html', {'form': form})
