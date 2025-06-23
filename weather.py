import requests
from datetime import datetime
import streamlit as st
import openai
import os
import pandas as pd
import altair as alt


def get_weather_data(city, weather_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()


def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()


def display_weekly_forecast(data):
    try:
        st.write("__________________________________________________")
        st.write("### weekly weather forecast")
        displayed_dates = set()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("", "Day")
        with c2:
            st.metric("", "Desc")
        with c3:
            st.metric("", "min_temp")
        with c4:
            st.metric("", "max_temp")

        for day in data["list"]:
            date = datetime.fromtimestamp(day["dt"]).strftime("%A, %B, %d")

            if date not in displayed_dates:
                displayed_dates.add(date)

                min_temp = day["main"]["temp_min"] - 273.15
                max_temp = day["main"]["temp_max"] - 273.15
                description = day["weather"][0]["description"]

                with c1:
                    st.write(f"{date}")

                with c2:
                    st.write(f"{description.capitalize()}")

                with c3:
                    st.write(f"{min_temp:.1f}degree C")

                with c4:
                    st.write(f"{max_temp:.1f}degree C")

    except Exception as e:
        st.error("Error in displaying weekly forecast: " + str(e))


def get_weather_data1(city, weather_api_key):
    if not weather_api_key:
        raise ValueError("Missing OpenWeatherMap API key")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(url)
    return response.json()


def get_weekly_forecast1(lat, lon, weather_api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}"
    response = requests.get(url)
    return response.json()


def generate_forecast_summary1(forecast_data, openai_api_key):
    openai.api_key = openai_api_key

    try:
        text_block = (
            "Give a natural language summary of the upcoming 5-day weather forecast:\n"
        )
        for entry in forecast_data["list"][: 5 * 8 : 8]:  # Every 24 hours (3h*8=24h)
            dt_txt = entry["dt_txt"]
            desc = entry["weather"][0]["description"]
            temp = entry["main"]["temp"]
            text_block += f"{dt_txt}: {desc}, {temp}°C\n"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a weather forecaster."},
                {"role": "user", "content": text_block},
            ],
        )

        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        st.error("OpenAI forecast generation failed: " + str(e))
        return None


def display_weekly_forecast1(forecast_data, summary):
    st.subheader("🗓️ Weekly Forecast Summary")
    if summary:
        st.success(summary)

    st.markdown("### 📅 Detailed Forecast")
    displayed_days = set()
    for entry in forecast_data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        if date not in displayed_days:
            displayed_days.add(date)
            time = entry["dt_txt"].split(" ")[1]
            desc = entry["weather"][0]["description"]
            temp_min = entry["main"]["temp_min"]
            temp_max = entry["main"]["temp_max"]
            st.write(
                f"**{date} ({time})**: {desc.capitalize()}, 🌡️ {temp_min:.1f}°C to {temp_max:.1f}°C"
            )


def get_air_pollution_data(lat, lon, weather_api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(url)
    return response.json()


def display_air_pollution(data):
    st.subheader("🌫️ Air Quality Index (AQI)")
    try:
        aqi = data["list"][0]["main"]["aqi"]
        pollutants = data["list"][0]["components"]

        aqi_text = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor 🤢",
        }

        st.metric("AQI Level", f"{aqi} - {aqi_text.get(aqi, 'Unknown')}")

        st.markdown("#### Pollutants (μg/m³):")
        for key, value in pollutants.items():
            st.write(f"**{key.upper()}**: {value}")

    except Exception as e:
        st.error("Error displaying air pollution data: " + str(e))


import pandas as pd
import altair as alt


def plot_forecast_chart(forecast_data):
    # Prepare data
    daily_data = []
    seen_dates = set()

    for entry in forecast_data["list"]:
        date_str = entry["dt_txt"].split(" ")[0]
        if date_str not in seen_dates:
            seen_dates.add(date_str)
            daily_data.append(
                {
                    "Date": date_str,
                    "Min Temp (°C)": entry["main"]["temp_min"],
                    "Max Temp (°C)": entry["main"]["temp_max"],
                    "Humidity (%)": entry["main"]["humidity"],
                    "Wind Speed (m/s)": entry["wind"]["speed"],
                }
            )

    df = pd.DataFrame(daily_data)

    st.subheader("📈 Temperature Forecast")
    temp_chart = (
        alt.Chart(df)
        .transform_fold(["Min Temp (°C)", "Max Temp (°C)"], as_=["Type", "Temperature"])
        .mark_line(point=True)
        .encode(x="Date:T", y="Temperature:Q", color="Type:N")
        .properties(width=700)
    )

    st.altair_chart(temp_chart)

    st.subheader("💧 Humidity & 🌬️ Wind Speed Forecast")
    hum_wind_chart = (
        alt.Chart(df)
        .transform_fold(["Humidity (%)", "Wind Speed (m/s)"], as_=["Type", "Value"])
        .mark_line(point=True)
        .encode(x="Date:T", y="Value:Q", color="Type:N")
        .properties(width=700)
    )

    st.altair_chart(hum_wind_chart)
