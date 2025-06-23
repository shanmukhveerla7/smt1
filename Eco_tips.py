import streamlit as st
import random

eco_tips = {
    "Water Saving": [
        "Turn off the tap while brushing your teeth. 🚿",
        "Fix dripping faucets to save thousands of liters. 💧",
        "Use a bucket instead of a hose for washing your car. 🚗",
    ],
    "Energy Efficiency": [
        "Switch off appliances when not in use. 🔌",
        "Use LED lights instead of incandescent bulbs. 💡",
        "Unplug chargers when not needed. ⚡",
    ],
    "Waste Reduction": [
        "Avoid single-use plastics. 🛍️",
        "Compost your food waste. 🌱",
        "Buy in bulk to reduce packaging waste. 📦",
    ],
    "Transportation": [
        "Use public transport or carpool when possible. 🚌",
        "Walk or cycle short distances. 🚶‍♀️🚴‍♂️",
        "Keep your tires inflated to save fuel. ⛽",
    ],
}


def eco_tips_module():
    st.title("🌿 Daily Eco Tips for Sustainable Living")

    # Category selection
    category = st.selectbox("Select a category", list(eco_tips.keys()))

    # Show a random tip
    if st.button("🌱 Show me a tip!"):
        tip = random.choice(eco_tips[category])
        st.success(tip)

    st.markdown("---")
    st.subheader("📢 Have your own eco tip?")
    user_tip = st.text_area("Share your eco-friendly habit or advice")
    if st.button("Submit Tip"):
        if user_tip.strip():
            st.success("✅ Thank you for your tip!")
            # Optional: Save to file or database
            with open("user_eco_tips.txt", "a", encoding="utf-8") as f:
                f.write(f"{category}: {user_tip}\n")
        else:
            st.warning("Please enter a valid tip.")
