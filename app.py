import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
# Replace 'YOUR_GEMINI_API_KEY' with your actual key from Google AI Studio
API_KEY = "AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Youth Sports Excellence", layout="wide")

# 2. UI Header & Branding
st.title("👟 CoachBot AI")
st.subheader("Empowering the Next Generation of Athletes")
st.markdown("Developed for **NextGen Sports Lab** to bridge the coaching gap.")
st.divider()

# 3. User Input Section (Task 2, Step 2)
with st.sidebar:
    st.header("Athlete Profile")
    sport = st.selectbox("Sport:", ["Football", "Cricket", "Basketball", "Athletics", "Rugby", "Tennis"])
    position = st.text_input("Position (e.g., Striker, Bowler):", "General")
    age = st.number_input("Age:", min_value=8, max_value=25, value=15)
    
    st.header("Physical Condition")
    injury_history = st.text_area("Injury History/Risk Zones:", "None")
    goal = st.selectbox("Primary Goal:", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength Training"])
    
    st.header("Preferences")
    nutrition_pref = st.radio("Dietary Type:", ["Veg", "Non-Veg", "Vegan"])
    # Hyperparameter Tuning (Task 2, Step 2)
    temp = st.slider("Coaching Style (Temperature):", 0.0, 1.0, 0.3) 

# 4. Compulsory Feature Design: 10 Prompts (Task 2, Step 3)
# These map to the 10-prompt requirement for "Distinguished" marks.
st.markdown("### Choose a Coaching Service")
feature_choice = st.selectbox("What do you need help with today?", [
    "Full-Body Workout Plan", 
    "Injury-Safe Recovery Routine", 
    "Positional Tactical Tips",
    "Weekly Nutrition Guide",
    "Match-Day Mindset & Visualization",
    "Warm-up & Cooldown Protocol",
    "Decision-Making Drills",
    "Stamina & Conditioning",
    "Hydration & Electrolyte Strategy",
    "Post-Match Recovery & Sleep"
])

# 5. Prompt Engineering Logic
# This dictionary contains the logic for the 10 features.
prompt_templates = {
    "Full-Body Workout Plan": f"Generate a full-body workout plan for a {age}-year-old {position} in {sport}. Goal: {goal}.",
    "Injury-Safe Recovery Routine": f"Create a safe recovery training schedule for an athlete with {injury_history} playing {sport}. Focus
