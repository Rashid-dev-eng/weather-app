from django.shortcuts import render
import requests
import datetime
from django.contrib import messages


def get_city_image(city):
    commons_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{city} city landmark",
        "gsrnamespace": 6,
        "gsrlimit": 1,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 1600,
    }
    headers = {
        "User-Agent": "WeatherApp/1.0"
    }

    try:
        response = requests.get(commons_url, params=params, headers=headers, timeout=8)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            image_info = page.get("imageinfo", [])
            if image_info:
                return image_info[0].get("thumburl") or image_info[0].get("url")
    except requests.RequestException:
        pass

    return None


def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = "London"  # Default city if none provided

    background_image = get_city_image(city)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4d339b7d7022e45073cf3f29195c0569"
    PARAMS = {'units': 'metric'}
    try:
        data = requests.get(url, PARAMS).json()
        
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        icon = data['weather'][0]['icon']
        today_date = datetime.date.today()
        day = today_date.strftime("%A")
        
        # day = datetime.date.today()
        return render(request, "weather/index.html", {
            "city": city,
            "description": description,
            "temp": temp,
            "icon": icon,
            "day": day,
            "date": today_date,
            

            
            "background_image": background_image,
        })
    except :
        messages.error(request, "City not found.")
        return render(request, "weather/index.html", {
            "city": city,
            "background_image": background_image,
        })
