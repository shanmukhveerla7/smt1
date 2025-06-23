import streamlit as st
import requests
import os


def get_traffic_data(lat, lon, tomtom_api_key):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={tomtom_api_key}"
    response = requests.get(url)
    return response.json()


def display_traffic_data(data):
    st.subheader("🚦 Traffic Flow")
    try:
        speed = data["flowSegmentData"]["currentSpeed"]
        free_flow_speed = data["flowSegmentData"]["freeFlowSpeed"]
        jam_factor = (
            data["flowSegmentData"]["currentTravelTime"]
            / data["flowSegmentData"]["freeFlowTravelTime"]
        )
        st.metric("Current Speed", f"{speed} km/h")
        st.metric("Free Flow Speed", f"{free_flow_speed} km/h")
        st.metric("Congestion Ratio", f"{jam_factor:.2f}")
    except Exception as e:
        st.error("Error fetching/displaying traffic data: " + str(e))
