import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
# Replace with your actual Gemini 1.5 API Key
API_KEY = "AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg" 

genai.configure(api_key=API_KEY)
# Using gemini-1.5-flash for speed and reliability
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Personal Excellence", layout="wide")

# 2. UI Header
st.title("👟 CoachBot AI")
st.subheader("High-Performance Personal Coaching")
st.markdown("Precision training and nutrition plans for the modern athlete.")
st.divider()

# 3. User Input Section (User Profile + Goal + Context)
with st.sidebar:
    st.header("👤 Athlete Profile")
    sport = st.selectbox("Sport:", ["Football", "Cricket", "Basketball", "Athletics", "Rugby", "Tennis"])
    position = st.text_input("Position/Role:", "Midfielder")
    age = st.number_input("Age:", min_value=8, max_value=25, value=16)
    
    st.header("🎯 Goals & Context")
    goal = st.selectbox("Primary Training Goal:", 
                        ["Build Stamina", "Strength & Power", "Injury Recovery", "Tactical IQ", "Speed & Agility"])
    injury_context = st.text_area("Medical Context (Injuries/Pain):", "None")
    
    st.header("🥗 Preferences")
    diet = st.radio("Dietary Requirement:", ["Non-Veg", "Veg", "Vegan"])
    
    # Low temperature for factual, consistent coaching
    temp = st.slider("Coach Strictness (Temperature):", 0.0, 1.0, 0.2) 

# 4. Feature Selection
st.markdown("### 📋 Select Coaching Service")
feature_choice = st.selectbox("What is our focus for this session?", [
    "7-Day Workout Split", 
    "Weekly Nutritional Meal Plan",
    "Injury-Specific Recovery Plan",
    "Positional Tactical Masterclass",
    "Match-Day Fueling & Hydration",
    "Skill-Based Drill Circuit"
])

# 5. Advanced Prompt Engineering (Persona + Profile + Context)
# This dictionary creates highly detailed instructions for the AI
prompt_templates = {
    "7-Day Workout Split": (
        f"Design a 7-day workout split in a Markdown Table. "
        f"Columns: Day, Focus Area, Exercises (with Sets/Reps), and Intensity Level. "
        f"Ensure the volume is age-appropriate for a {age}-year-old."
    ),
    "Weekly Nutritional Meal Plan": (
        f"Create a high-performance {diet} meal plan in a Markdown Table. "
        f"Columns: Day, Breakfast, Lunch, Post-Training Snack, Dinner. "
        f"Optimize macros for a {sport} {position} aiming to {goal}."
    ),
    "Injury-Specific Recovery Plan": (
        f"Create a rehabilitation schedule in a Markdown Table. "
        f"Columns: Phase, Exercise/Movement, Duration, and Pain-Threshold Guide. "
        f"Context: Athlete has {injury_context}. Avoid high-impact if necessary."
    ),
    "Positional Tactical Masterclass": (
        f"Provide a tactical breakdown for a {position} in {sport} in a Markdown Table. "
        f"Columns: Game Scenario, Recommended Action, Key Movement, Common Mistake to Avoid."
    ),
    "Match-Day Fueling & Hydration": (
        f"Create a match-day timeline in a Markdown Table. "
        f"Columns: Time (Relative to Kickoff), Nutrition/Fluid, Purpose, Electrolyte Needs."
    ),
    "Skill-Based Drill Circuit": (
        f"Design 4 technical drills for {position} skills in a Markdown Table. "
        f"Columns: Drill Name, Setup/Equipment, Execution Steps, Goal Reps/Time."
    )
}

# 6. Execution & Table Rendering
if st.button("Generate My Personal Plan"):
    with st.spinner("Your coach is preparing your plan..."):
        
        # Defining the "Personal Coach" Persona
        persona_prefix = (
            f"Act as an elite personal sports coach. I am a {age}-year-old {sport} player "
            f"specializing as a {position}. My goal is {goal}. "
            f"Contextual constraints: {injury_context}. "
            f"STRICT RULES: 1. Provide the response primarily as a Markdown Table. "
            f"2. Be concise. 3. No long intros. 4. Use professional coaching terminology."
        )
        
        full_prompt = f"{persona_prefix}\n\nTask: {prompt_templates[feature_choice]}"
        
        try:
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            st.markdown(f"### ⚡ Your Personal {feature_choice}")
            # Streamlit handles the Markdown table automatically
            st.markdown(response.text)
            
            # Simple visualization for visual impact
            if "Nutritional" in feature_choice:
                st.info("💡 Tip: Ensure you are drinking at least 3-4 liters of water on training days.")
                
        except Exception as e:
            st.error(f"Coaching Error: {e}")

st.divider()
st.caption("Note: These plans are AI-generated. For rehabilitation, always consult a physical therapist.")
