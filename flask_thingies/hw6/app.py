from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")#я так і не розібрався як воно там
CITY = "Kyiv"
UNITS = "metric"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}&lang=ua"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def recommend_pizza(weather_main):
    if weather_main == "Rain":
        return "Дощ, піца з грибами або гостру пепероні"
    elif weather_main == "Clear":
        return "Ясно, маргарита з моцарелою"
    elif weather_main == "Snow":
        return "Сніжно, піца з чотирма сирами"
    elif weather_main == "Clouds":
        return "Хмарно? Піца з беконом і карамелізованою цибулею"
    else:
        return "Піца — завжди гарна ідея"

@app.route('/')
def index():
    weather = get_weather(CITY)
    if weather:
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        weather_main = weather['weather'][0]['main']
        recommendation = recommend_pizza(weather_main)
        return render_template('index.html',
                               temp=temp,
                               description=description,
                               city=CITY,
                               recommendation=recommendation,
                               date=datetime.now().strftime('%Y-%m-%d'))
    else:
        return render_template('index.html', error="Не вдалося отримати погоду.")

if __name__ == '__main__':
    app.run(debug=True)
