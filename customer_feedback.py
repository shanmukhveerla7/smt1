import streamlit as st
import pandas as pd
import os
from datetime import datetime


def feedback_form():
    st.title("📋 Share Your Feedback")

    name = st.text_input("👤 Name")
    city = st.text_input("🏙️ City")
    rating = st.slider("⭐ Rate your experience (1-5)", 1, 5, 3)
    feedback = st.text_area("📝 Your Feedback", height=150)

    if st.button("Submit Feedback"):
        if name.strip() == "" or feedback.strip() == "":
            st.warning("⚠️ Please fill in your name and feedback.")
        else:
            st.success("✅ Thank you for your valuable feedback!")
            st.balloons()

            # Save to CSV
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback_data = {
                "timestamp": timestamp,
                "name": name,
                "city": city,
                "rating": rating,
                "feedback": feedback,
            }

            file_path = "feedback_data.csv"
            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path)
                df_new = pd.DataFrame([feedback_data])
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = pd.DataFrame([feedback_data])

            df_combined.to_csv(file_path, index=False)
