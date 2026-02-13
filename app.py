import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
# Replace with your actual Gemini 1.5 API Key from Google AI Studio
API_KEY = "AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg" 

genai.configure(api_key=API_KEY)
# Using Gemini 1.5 Pro as per assignment requirements 
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Youth Sports Excellence", layout="wide")

# 2. UI Header & Branding (Task 2, Step 1)
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
    # Lower temperature (~0.3) for conservative/safe training plans 
    temp = st.slider("Coaching Style (Temperature):", 0.0, 1.0, 0.3) 

# 4. Compulsory Feature Design: 10 Prompts (Task 2, Step 3)
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

# 5. Corrected Prompt Engineering Logic (Task 2, Step 3)
# All f-strings and brackets are now properly closed to avoid SyntaxErrors
prompt_templates = {
    "Full-Body Workout Plan": f"Generate a full-body workout plan for a {age}-year-old {position} in {sport}. Goal: {goal}.",
    "Injury-Safe Recovery Routine": f"Create a safe recovery training schedule for an athlete with {injury_history} playing {sport}. Focus on low-impact adaptations.",
    "Positional Tactical Tips": f"Provide tactical coaching tips to improve skill and positioning for a {position} in {sport}.",
    "Weekly Nutrition Guide": f"Suggest a week-long nutrition guide for a {age}-year-old athlete following a {nutrition_pref} diet. Include a table of daily macros.",
    "Match-Day Mindset & Visualization": f"Provide pre-match visualization techniques and mental focus routines for a {age}-year-old {sport} player.",
    "Warm-up & Cooldown Protocol": f"Generate a personalized warm-up and cooldown routine for a {sport} {position}.",
    "Decision-Making Drills": f"Design positional decision-making drills for a {position} in {sport} to improve game IQ.",
    "Stamina & Conditioning": f"Create a high-intensity interval training (HIIT) plan specifically to build stamina for {sport}.",
    "Hydration & Electrolyte Strategy": f"Generate a hydration and electrolyte scheduling guide for intense {sport} training sessions.",
    "Post-Match Recovery & Sleep": f"Suggest mobility workouts and sleep hygiene tips for optimal recovery after a {sport} tournament."
}

# 6. Execution & Output (Task 2, Step 4 & 6)
if st.button("Get CoachBot Advice"):
    with st.spinner("CoachBot is analyzing your profile..."):
        # Persona-style instruction to ensure high-quality output 
        full_prompt = f"""
        System: Act as a professional youth sports coach. 
        Athlete: {age} years old, Sport: {sport}, Position: {position}.
        Medical Note: {injury_history}.
        Request: {prompt_templates[feature_choice]}
        Output: Provide structured, safe, and motivating advice.
        """
        
        try:
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            st.markdown("---")
            st.markdown(f"## 📋 {feature_choice}")
            st.write(response.text)

            # Optional Visualization (Task 2, Step 6)
            if "Nutrition" in feature_choice or "Hydration" in feature_choice:
                st.subheader("Recommended Macro/Hydration Distribution")
                labels = ['Protein/Water', 'Carbs/Electrolytes', 'Fats/Vitamins']
                values = [25, 55, 20]
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(labels, values, color=['#FF4B4B', '#1C83E1', '#00C0F2'])
                ax.set_ylabel('Percentage (%)')
                st.pyplot(fig)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()
st.caption("Disclaimer: CoachBot AI provides general suggestions. Always consult a professional coach or doctor for serious injuries.")
