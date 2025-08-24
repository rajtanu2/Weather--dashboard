import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="🌦 Real-Time Weather Dashboard", layout="wide")

st.title("🌦 Real-Time Weather Dashboard with Graphs")

# user input
city = st.text_input("Enter city name", "Mumbai")

if city:
    # 👉 सुरक्षितरीत्या secrets मधून API key घे
    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # current weather
        st.subheader(f"📍 Current Weather in {city}")
        current = data["list"][0]
        temp = current["main"]["temp"]
        desc = current["weather"][0]["description"]
        st.write(f"🌡 Temperature: {temp}°C")
        st.write(f"☁ Condition: {desc}")

        # hourly temperature data
        h = pd.DataFrame([{
            "time": pd.to_datetime(item["dt"], unit="s", utc=True),
            "temp": item["main"]["temp"]
        } for item in data["list"]])

        h.set_index("time", inplace=True)

        # UTC time handling
        now = pd.Timestamp.utcnow().tz_convert("UTC")

        st.subheader("🕒 Hourly Temperature (Next 72 Hours)")
        st.line_chart(h.tail(72))

        # daily avg temp
        d = h.resample("D").mean()
        st.subheader("📅 Daily Average Temperature")
        st.bar_chart(d)

    else:
        st.error("❌ City not found or API issue.")
