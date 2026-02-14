import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
# SECURITY NOTE: Never hardcode API keys in production!
API_KEY = "AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg" 

genai.configure(api_key=API_KEY)
# Updated to a valid model name
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Youth Sports Excellence", layout="wide")

# 2. UI Header
st.title("👟 CoachBot AI")
st.subheader("Concise, Table-Based Athlete Support")
st.divider()

# 3. User Input Section
with st.sidebar:
    st.header("Athlete Profile")
    sport = st.selectbox("Sport:", ["Football", "Cricket", "Basketball", "Athletics", "Rugby", "Tennis"])
    position = st.text_input("Position:", "General")
    age = st.number_input("Age:", min_value=8, max_value=25, value=15)
    
    st.header("Physical Condition")
    injury_history = st.text_area("Injury History:", "None")
    goal = st.selectbox("Primary Goal:", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength Training"])
    
    st.header("Preferences")
    nutrition_pref = st.radio("Dietary Type:", ["Veg", "Non-Veg", "Vegan"])
    
    temp = st.slider("Coaching Style (Strict -> Creative):", 0.0, 1.0, 0.2) 

# 4. Refined Prompt Engineering (Enforcing Tables & Brevity)
st.markdown("### Choose a Coaching Service")
feature_choice = st.selectbox("What do you need help with today?", [
    "Full-Body Workout Plan", 
    "Weekly Nutrition Guide",
    "Injury-Safe Recovery Routine", 
    "Positional Tactical Tips",
    "Warm-up & Cooldown Protocol",
    "Decision-Making Drills",
    "Stamina & Conditioning",
    "Hydration & Electrolyte Strategy"
])

# Updated templates to specifically ask for Markdown Tables
prompt_templates = {
    "Full-Body Workout Plan": "Create a 4-day workout split in a Markdown Table. Columns: Day, Exercise, Sets/Reps, Focus.",
    "Weekly Nutrition Guide": f"Create a 7-day {nutrition_pref} meal plan in a Markdown Table. Columns: Day, Breakfast, Lunch, Dinner, Snack.",
    "Injury-Safe Recovery Routine": f"Provide a low-impact recovery schedule in a Markdown Table considering {injury_history}. Columns: Phase, Exercise, Duration, Safety Note.",
    "Positional Tactical Tips": "Provide 5 bullet-pointed tactical tips for this position. Be extremely brief.",
    "Warm-up & Cooldown Protocol": "Create a pre/post session routine in a Markdown Table. Columns: Phase, Exercise, Time, Purpose.",
    "Decision-Making Drills": "List 3 drills in a Markdown Table. Columns: Drill Name, Setup, Objective.",
    "Stamina & Conditioning": "Create a weekly HIIT schedule in a Markdown Table. Columns: Day, Activity, Intensity, Rest.",
    "Hydration & Electrolyte Strategy": "Create a hydration timeline in a Markdown Table. Columns: Timing (Pre/During/Post), Fluid Amount, Electrolyte Need."
}

# 5. Execution & Output
if st.button("Get CoachBot Advice"):
    with st.spinner("Generating your concise plan..."):
        # The System Instruction now strictly enforces the "Concise" and "Table" rules
        system_instruction = (
            "You are a professional youth sports coach. Your responses MUST be concise. "
            "If a table is requested, use Markdown Table format. Use bullet points for lists. "
            "Avoid long introductions or conclusions. Get straight to the data."
        )
        
        full_prompt = f"""
        {system_instruction}
        Athlete: {age}yo {sport} player ({position}). Goal: {goal}. 
        Request: {prompt_templates[feature_choice]}
        """
        
        try:
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            st.markdown("---")
            st.markdown(f"## 📋 {feature_choice}")
            
            # Display the AI response (Gemini's Markdown tables render perfectly in st.write)
            st.write(response.text)

            # 6. Visualization
            if any(x in feature_choice for x in ["Nutrition", "Hydration", "Workout"]):
                st.subheader("Target Distribution")
                labels = ['Intensity/Protein', 'Recovery/Carbs', 'Mobility/Fats']
                values = [35, 45, 20]
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.barh(labels, values, color=['#FF4B4B', '#1C83E1', '#00C0F2'])
                st.pyplot(fig)
                
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Disclaimer: CoachBot AI provides general suggestions. Consult a pro for medical advice.")
