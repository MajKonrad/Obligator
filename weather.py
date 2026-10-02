import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 59.92,
    "longitude": 10.73,
    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
    "timezone": "Europe/Oslo"
}
def get_updated_weather():
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_todays_weather():
    data = get_updated_weather()

    todays_max_temp = data["daily"]["temperature_2m_max"][0]
    todays_min_temp = data["daily"]["temperature_2m_min"][0]
    todays_precipitation = data["daily"]["precipitation_sum"][0]
    todays_max_wind = data["daily"]["wind_speed_10m_max"][0]
    todays_weather_code = data["daily"]["weather_code"][0]

    average_temp = round((todays_min_temp + todays_max_temp) / 2, 1)
    todays_weather = weather_code_to_text(todays_weather_code)

    return (
        f"🌤️ Været ved OsloMet i dag\n\n"
        f"🌡️ Temperatur: {todays_min_temp}°C - {todays_max_temp}°C\n"
        f"📊 Midtpunkt: {average_temp}°C\n"
        f"🌧️ Nedbør: {todays_precipitation} mm\n"
        f"💨 Maks vind: {todays_max_wind} km/t\n"
        f"{todays_weather}"
    )


def get_tomorrows_weather():
    data = get_updated_weather()

    tomorrows_max_temp = data["daily"]["temperature_2m_max"][1]
    tomorrows_min_temp = data["daily"]["temperature_2m_min"][1]
    tomorrows_precipitation = data["daily"]["precipitation_sum"][1]
    tomorrows_max_wind = data["daily"]["wind_speed_10m_max"][1]
    tomorrows_weather_code = data["daily"]["weather_code"][1]

    average_temp = round((tomorrows_min_temp + tomorrows_max_temp) / 2, 1)
    tomorrows_weather = weather_code_to_text(tomorrows_weather_code)

    return (
        f"🌤️ Været ved OsloMet i morgen\n\n"
        f"🌡️ Temperatur: {tomorrows_min_temp}°C - {tomorrows_max_temp}°C\n"
        f"📊 Midtpunkt: {average_temp}°C\n"
        f"🌧️ Nedbør: {tomorrows_precipitation} mm\n"
        f"💨 Maks vind: {tomorrows_max_wind} km/t\n"
        f"{tomorrows_weather}"
    )

def weather_code_to_text(code):
    if code == 0:
        return "☀️ Klarvær"
    elif code == 1:
        return "🌤️ For det meste klart"
    elif code == 2:
        return "⛅ Delvis skyet"
    elif code == 3:
        return "☁️ Overskyet"
    elif code in [45, 48]:
        return "🌫️ Tåke"
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️ Regn"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "❄️ Snø"
    elif code in [95, 96, 99]:
        return "⛈️ Tordenvær"
    else:
        return "❓ Ukjent vær"

