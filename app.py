import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from weather import (
    get_weather_data,
    get_weekly_forecast,
    display_weekly_forecast,
    get_air_pollution_data,
    display_air_pollution,
    plot_forecast_chart,
)
from traffic import get_traffic_data, display_traffic_data
from chatbot import run_chatbot
from summarizer import run_summarizer
from KPI_forecast import kpi_forecast
from customer_feedback import feedback_form
from Anomoly_detection import anomaly_detection
from Eco_tips import eco_tips_module


# -------------------- Custom Background & Styling --------------------
st.markdown(
    """
    <style>
        body {
            background-color: #f7fafd;
        }
        .stApp {
            background-image: linear-gradient(to bottom right, #e6f0ff, #fef9ff);
        }
        .title {
            font-size: 26px;
            font-weight: bold;
            color: #003366;
        }
        .section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# -------------------- Main Dashboard --------------------
def main():
    st.set_page_config(page_title="Smart City Assistant", layout="wide")
    st.sidebar.title("🧭 Smart City Assistant")

    selected_module = st.sidebar.radio(
        "📚 Choose a Module",
        [
            "🌦️ Weather Forecast",
            "🌫️ Air Pollution",
            "🚦 Traffic Monitor",
            "📝 Policy Summarizer",
            "🤖 Chat Assistant",
            "📊 KPI Forecast 📈",
            "🚨 Anomaly Detection",
            "🗣️ Customer Feedback ",
            "🌿 Eco Tips",
        ],
    )

    if selected_module == "🌦️ Weather Forecast":
        st.markdown(
            '<div class="section"><div class="title">🌦️ Weather Forecast Module</div>',
            unsafe_allow_html=True,
        )
        city = st.text_input("🏙️ Enter City", "London")
        if st.button("📡 Get Weather"):
            api_key = os.getenv("openweathermap_api")
            weather_data = get_weather_data(city, api_key)
            if weather_data.get("cod") != 404:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                forecast_data = get_weekly_forecast(api_key, lat, lon)
                st.success(f"✅ Live Weather in {city}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{weather_data['main']['temp'] - 273.15:.2f}°C",
                    )
                    st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("📊 Pressure", f"{weather_data['main']['pressure']} hPa")
                    st.metric("🌬️ Wind Speed", f"{weather_data['wind']['speed']} m/s")
                display_weekly_forecast(forecast_data)
                plot_forecast_chart(forecast_data)
            else:
                st.error("🚫 City not found.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🌫️ Air Pollution":
        st.markdown(
            '<div class="section"><div class="title">🌫️ Air Quality Index Monitor</div>',
            unsafe_allow_html=True,
        )
        city = st.text_input("🏙️ Enter City for AQI", "Delhi")
        if st.button("🔍 Get AQI"):
            api_key = os.getenv("openweathermap_api")
            weather_data = get_weather_data(city, api_key)
            if weather_data.get("cod") != 404:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                pollution_data = get_air_pollution_data(lat, lon, api_key)
                display_air_pollution(pollution_data)
            else:
                st.error("🚫 City not found.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🚦 Traffic Monitor":
        st.markdown(
            '<div class="section"><div class="title">🚦 Real-Time Traffic Monitoring</div>',
            unsafe_allow_html=True,
        )
        city = st.text_input("🚗 City for Traffic", "Hyderabad")
        if st.button("🛰️ Get Traffic Data"):
            weather_api_key = os.getenv("openweathermap_api")
            tomtom_api_key = os.getenv("TOMTOM_API_KEY")
            weather_data = get_weather_data(city, weather_api_key)
            if weather_data.get("cod") != 404:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                traffic_data = get_traffic_data(lat, lon, tomtom_api_key)
                display_traffic_data(traffic_data)
            else:
                st.error("🚫 City not found.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "📝 Policy Summarizer":
        st.markdown(
            '<div class="section"><div class="title">📝 Policy Summarizer</div>',
            unsafe_allow_html=True,
        )
        run_summarizer()
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🤖 Chat Assistant":
        st.markdown(
            '<div class="section"><div class="title">🤖 Smart City Chatbot</div>',
            unsafe_allow_html=True,
        )
        run_chatbot()
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "📊 KPI Forecast 📈":
        st.markdown(
            '<div class="section"><div class="title">📊 Key Performance Indicator Forecast</div>',
            unsafe_allow_html=True,
        )
        kpi_forecast()
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🗣️ Customer Feedback ":
        st.markdown(
            '<div class="section"><div class="title">🗣️ Customer Feedback Portal</div>',
            unsafe_allow_html=True,
        )
        feedback_form()
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🚨 Anomaly Detection":
        st.markdown(
            '<div class="section"><div class="title">🚨 Anomaly Detection</div>',
            unsafe_allow_html=True,
        )
        anomaly_detection()
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_module == "🌿 Eco Tips":
        eco_tips_module()


if __name__ == "__main__":
    main()
