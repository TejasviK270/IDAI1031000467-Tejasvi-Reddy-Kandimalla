import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

# 1. Configuration & API Setup
API_KEY = "AIzaSyDE7UZV65V1r3Ak9zRf5MCtxBPqoULIBVg" # 

genai.configure(api_key=API_KEY)
# Using gemini-2.5-flash for high-speed, reliable structured output
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="CoachBot AI: Elite Performance", layout="wide")

# 2. UI Header
st.title("👟 CoachBot AI")
st.subheader("Personalized Athletic Coaching & Consultation")
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
    
    # Low temperature (0.1-0.2) is critical for strict formatting consistency
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
        "7-Day Workout Split": f"Create a 7-day workout split for a {age}yo {position} in {sport}. Format as a Markdown Table with columns [Day, Focus, Exercises, Intensity].",
        "Weekly Nutritional Meal Plan": f"Create a high-performance {diet} meal plan. Format as a Markdown Table with columns [Day, Breakfast, Lunch, Snack, Dinner].",
        "Injury-Specific Recovery Plan": f"Create a rehab schedule for {injury_context}. Format as a Markdown Table with columns [Phase, Exercise, Duration, Safety Guide].",
        "Positional Tactical Masterclass": f"Provide tactical tips for a {position} in {sport}. Format as a Markdown Table with columns [Scenario, Action, Movement, Common Error].",
        "Match-Day Fueling & Hydration": f"Match-day timeline as a Markdown Table with columns [Time, Intake, Purpose]."
    }
    
    generate_standard = st.button("Generate Service Plan")

with tabs[1]:
    st.markdown("### 💬 Custom Coach Consultation")
    user_query = st.text_input("Ask your coach anything:")
    generate_custom = st.button("Ask CoachBot")

# 5. Centralized Execution Logic
if generate_standard or generate_custom:
    # This prefix forces the API to prioritize the table format over paragraphs
    persona_prefix = (
        f"You are an elite personal coach. Athlete: {age}yo {sport} ({position}). "
        f"Goal: {goal}. Context: {injury_context}. "
        f"STRICT RULES: 1. Output MUST be a Markdown Table. 2. NO paragraphs. 3. NO long intros. 4. Professional terminology only."
    )

    if generate_standard:
        final_prompt = f"{persona_prefix}\n\nTask: {prompt_templates[feature_choice]}"
        title = feature_choice
    else:
        final_prompt = f"{persona_prefix}\n\nUser Question: {user_query}\n\nRule: Answer ONLY in a Markdown Table format."
        title = "Coach Consultation"

    with st.spinner("Analyzing profile and generating response..."):
        try:
            response = model.generate_content(
                final_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temp)
            )
            
            # Formatting Logic: Ensure the table renders correctly
            raw_text = response.text
            # Force a blank line before the table syntax (required for Streamlit rendering)
            clean_output = raw_text.strip().replace("|", "\n\n|", 1) if not raw_text.startswith("\n") else raw_text
            
            st.markdown("---")
            st.markdown(f"### ⚡ Your Personal {title}")
            
            # Markdown is the most reliable way to display AI-generated tables in Streamlit
            st.markdown(clean_output)
            
            if "Nutrition" in title or "Meal" in raw_text:
                st.info("💡 Pro-Tip: Hydration is just as vital as nutrition. Aim for 3-4 liters daily.")
                
        except Exception as e:
            st.error(f"Coaching Error: {e}")

st.divider()
st.caption("CoachBot AI | Created for NextGen Sports Lab | Note: Always consult a professional for medical advice.")
