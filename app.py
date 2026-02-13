import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuration & API Setup
st.set_page_config(page_title="CoachBot AI: Youth Sports Excellence", layout="wide")

# Securely handle API Key (In production, use Streamlit Secrets)
api_key = st.sidebar.text_input("AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.warning("Please enter your Gemini API Key in the sidebar to begin.")

# 2. UI Header
st.title("👟 CoachBot AI")
st.subheader("Empowering the Next Generation of Athletes")
st.markdown("---")

# 3. User Input Section (Task 2, Step 2)
col1, col2 = st.columns(2)

with col1:
    sport = st.selectbox("Select Your Sport:", ["Football", "Cricket", "Basketball", "Athletics", "Rugby"])
    position = st.text_input("Your Position (e.g., Striker, Bowler, Point Guard):")
    age = st.number_input("Age:", min_value=8, max_value=25, value=15)
    training_pref = st.select_slider("Training Intensity:", options=["Low", "Moderate", "High", "Pro"])

with col2:
    injury_history = st.text_area("Injury History / Risk Zones (e.g., Ankle sprain, none):", "None")
    nutrition_pref = st.radio("Nutrition Preference:", ["Veg", "Non-Veg", "Vegan"])
    goal = st.selectbox("Primary Goal:", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength Training"])

# Hyperparameter Tuning (Task 2, Step 2)
st.sidebar.header("Model Settings")
temp = st.sidebar.slider("Creativity (Temperature):", 0.0, 1.0, 0.3) # Lower for safer plans 

# 4. Features & Prompt Engineering (Task 2, Step 3)
# We map features to specific prompts as required by the assignment brief
feature_map = {
    "Full Workout Plan": f"Generate a detailed full-body workout plan for a {age} year old {position} in {sport}. Current goal: {goal}.",
    "Injury-Safe Recovery": f"Create a safe recovery training schedule for a {sport} athlete with {injury_history}. Focus on low-impact but effective movement.",
    "Tactical Advice": f"Provide elite tactical coaching tips to improve decision-making as a {position} in {sport}.",
    "Nutrition & Macros": f"Suggest a daily nutrition guide for a {age} year old athlete on a {nutrition_pref} diet. Provide data in a table format with Protein, Carbs, and Fats in grams.",
    "Warm-up/Cooldown": f"Generate a personalized 15-minute warm-up and 10-minute cooldown routine specifically for a {position} in {sport}."
}

selected_feature = st.selectbox("Choose CoachBot Service:", list(feature_map.keys()))

if st.button("Generate Coaching Advice"):
    if not api_key:
        st.error("API Key missing.")
    else:
        with st.spinner("CoachBot is analyzing your profile..."):
            # Constructing the Persona-style Prompt (Task 2, Step 5)
            context_prompt = f"""
            You are an expert youth sports coach. Speak in a motivating, professional, and safety-conscious tone.
            User Profile: {age} year old {sport} player ({position}). 
            Health Note: {injury_history}.
            Task: {feature_map[selected_feature]}
            Instructions: If providing nutrition, ensure it's safe for a youth athlete. If providing workouts, emphasize form.
            """
            
            response = model.generate_content(
                context_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            # 5. Output Formatting & Optional Visualizations (Task 2, Step 4 & 6)
            st.markdown("### 📋 Your Personalized Coaching Output")
            st.write(response.text)

            # Optional: If Nutrition is selected, show a mock Macro Chart (Requirement Step 6)
            if "Nutrition" in selected_feature:
                st.markdown("---")
                st.subheader("Typical Macro Distribution for your Goal")
                # Sample data for visualization purposes
                labels = ['Protein', 'Carbohydrates', 'Fats']
                sizes = [25, 55, 20] # General athletic distribution
                
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
                ax.axis('equal') 
                st.pyplot(fig)

# 6. Deployment Footer
st.markdown("---")
st.info("Developed for NextGen Sports Lab - Bridging the coaching gap through AI.")
