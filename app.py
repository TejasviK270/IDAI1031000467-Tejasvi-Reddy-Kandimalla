import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configure Gemini API
genai.configure(api_key="AIzaSyBlJ0FSupoYW8NrsxXsZQyDehDLzbwV-N4")

# Try to load the best available model
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")
except Exception:
    # Fallback if 1.5-pro is not available
    model = genai.GenerativeModel("models/gemini-pro")

# Streamlit UI
st.title("🏋️ CoachBot AI - Smart Fitness Assistant")
st.write("Personalized fitness, nutrition, and tactical advice powered by Generative AI.")

# Collect user input
sport = st.selectbox("Select your sport:", ["Football", "Cricket", "Basketball", "Athletics"])
position = st.text_input("Enter your position (e.g., Striker, Bowler, Goalkeeper)")
injury = st.text_input("Injury history or risk zones (optional)")
training_pref = st.selectbox("Training preference:", ["Low Intensity", "Moderate", "High Intensity"])
nutrition = st.text_input("Nutrition requirements (e.g., vegetarian, high protein, allergies)")
goal = st.text_input("Desired goal (e.g., stamina, recovery, tactical improvement)")

if st.button("Generate Plan"):
    # Build the prompt
    prompt = f"""
    You are CoachBot AI, a virtual sports coach.
    Sport: {sport}
    Position: {position}
    Injury history: {injury}
    Training preference: {training_pref}
    Nutrition: {nutrition}
    Goal: {goal}

    Generate a personalized fitness plan including:
    - Workout routine
    - Recovery tips
    - Tactical advice
    - Nutrition guidance
    """

    try:
        response = model.generate_content([prompt])  # wrap prompt in list
        st.subheader("🏆 Your Personalized Plan")
        st.write(response.text)
    except Exception as e:
        st.error(f"Gemini API error: {e}")
