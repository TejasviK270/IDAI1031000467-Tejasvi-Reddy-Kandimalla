import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
API_KEY = "AIzaSyCGxBAiSzN7drX1y72lWj7osKhOGPoeEeQ" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Elite Performance", layout="wide")

# 2. UI Header
st.title("👟 CoachBot AI")
st.subheader("High-Performance Personal Coaching & AI Consultation")
st.divider()

# 3. User Input Section (Profile + Goal + Context)
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
    
    temp = st.slider("Coach Strictness (Temperature):", 0.0, 1.0, 0.2) 

# 4. Feature Selection
tabs = st.tabs(["Standard Services", "Ask Coach Anything"])

with tabs[0]:
    st.markdown("### 📋 Select Coaching Service")
    feature_choice = st.selectbox("Choose a focused plan:", [
        "7-Day Workout Split", 
        "Weekly Nutritional Meal Plan",
        "Injury-Specific Recovery Plan",
        "Positional Tactical Masterclass",
        "Match-Day Fueling & Hydration"
    ])

    prompt_templates = {
        "7-Day Workout Split": f"Design a 7-day workout split in a Markdown Table. Columns: Day, Focus, Exercises (Sets/Reps), and Intensity. Age-appropriate for {age}.",
        "Weekly Nutritional Meal Plan": f"Create a high-performance {diet} meal plan in a Markdown Table. Columns: Day, Breakfast, Lunch, Snack, Dinner. Goal: {goal}.",
        "Injury-Specific Recovery Plan": f"Create a rehab schedule in a Markdown Table. Columns: Phase, Exercise, Duration, and Safety Guide. Context: {injury_context}.",
        "Positional Tactical Masterclass": f"Tactical breakdown for {position} in {sport} in a Markdown Table. Columns: Scenario, Action, Movement, Common Error.",
        "Match-Day Fueling & Hydration": f"Match-day timeline in a Markdown Table. Columns: Time, Nutrition/Fluid, Purpose."
    }
    
    generate_standard = st.button("Generate Service Plan")

with tabs[1]:
    st.markdown("### 💬 Custom Coach Consultation")
    user_query = st.text_input("Ask your coach anything (e.g., 'How to improve my sprint start?' or 'Best stretches for lower back'):")
    generate_custom = st.button("Ask CoachBot")

# 5. Centralized Execution Logic
if generate_standard or generate_custom:
    # Build the strict persona
    persona_prefix = (
        f"Act as an elite personal sports coach. Athlete: {age}yo {sport} player ({position}). "
        f"Goal: {goal}. Medical Context: {injury_context}. "
        f"STRICT RULES: 1. Be concise. 2. Use Markdown Tables for plans/schedules. 3. No long intros. 4. Use professional terminology."
    )

    # Determine which prompt to use
    if generate_standard:
        final_prompt = f"{persona_prefix}\n\nTask: {prompt_templates[feature_choice]}"
        title = feature_choice
    else:
        final_prompt = f"{persona_prefix}\n\nUser Question: {user_query}\n\nInstruction: Answer concisely. Use a table if the data allows for it."
        title = "Coach Consultation"

    with st.spinner("Analyzing profile and generating response..."):
        try:
            response = model.generate_content(
                final_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            st.markdown("---")
            st.markdown(f"### ⚡ Your Personal {title}")
            st.markdown(clean_response)
            
            # Simple visualization logic
            if "Nutrition" in title or "Meal" in response.text:
                st.info("💡 Pro-Tip: Ensure consistent sleep (8-9 hours) to maximize this nutrition plan.")
                
        except Exception as e:
            st.error(f"Coaching Error: {e}")

st.divider()
st.caption("Disclaimer: CoachBot AI provides suggestions. Consult a medical professional for serious injuries.")
