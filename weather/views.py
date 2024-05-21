from django.shortcuts import render
import requests
from datetime import datetime

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
