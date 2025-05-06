from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b3ef2b1acf591382c5b91024b4c68f3b"  # 替换为你的 API 密钥

def get_5_day_forecast(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "未知错误")}

        forecast_list = []
        for item in data['list']:
            dt_txt = item['dt_txt']
            temp = item['main']['temp']
            feels_like = item['main']['feels_like']
            humidity = item['main']['humidity']
            weather_desc = item['weather'][0]['description']

            forecast_list.append({
                'time': dt_txt,
                'temp': temp,
                'feels_like': feels_like,
                'humidity': humidity,
                'desc': weather_desc
            })

        return {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'forecast': forecast_list
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        city = request.form.get("city")
        result = get_5_day_forecast(city)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)