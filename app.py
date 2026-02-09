import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configure Gemini API with your key
genai.configure(api_key="AIzaSyD4OtdbrAP5zSPmW5XDxsVSciBWVAchAG0")

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

# Button to generate outputs
if st.button("Generate Plan"):
    # Define 10 compulsory prompts
    prompts = [
        f"Generate a full-body workout plan for a {position} in {sport}.",
        f"Create a safe recovery training schedule for an athlete with {injury}.",
        f"Provide tactical coaching tips to improve performance in {sport}.",
        f"Suggest a week-long nutrition guide for a 15-year-old athlete following {nutrition}.",
        f"Generate a personalized warm-up and cooldown routine for a {position} in {sport}.",
        f"Design a hydration and electrolyte strategy for a young {sport} athlete.",
        f"Create mental focus routines for a player preparing for a tournament.",
        f"Provide mobility workouts for post-injury recovery targeting {injury}.",
        f"Generate positional decision-making drills for a {position} in {sport}.",
        f"Suggest pre-match visualization techniques to improve confidence and tactical awareness."
    ]

    # Loop through prompts and display outputs
    for p in prompts:
        try:
            response = model.generate_content([p])
            st.subheader("Prompt")
            st.write(p)
            st.subheader("Output")
            st.write(response.text)
            st.write("---")
        except Exception as e:
            st.error(f"Gemini API error: {e}")
