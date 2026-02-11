import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import textwrap

# Configure Gemini API
genai.configure(api_key="AIzaSyDB9wFirBoOWOJCjstVxVEXXROgFtyfr-I")

# Load model with fallback
try:
    model = genai.GenerativeModel("models/gemini-1.5-pro")
except Exception:
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

# Free-form custom prompt
custom_prompt = st.text_area("Or enter your own custom coaching request:")

if st.button("Generate Plan"):
    # Build structured prompt if no custom prompt is given
    if custom_prompt.strip():
        prompt = custom_prompt
    else:
        prompt = f"""
        You are CoachBot AI, a virtual sports coach.
        Sport: {sport}
        Position: {position}
        Injury history: {injury}
        Training preference: {training_pref}
        Nutrition: {nutrition}
        Goal: {goal}

        Generate a concise fitness plan in 4–5 sentences only.
        Keep the style similar to:
        "Start with 15 minutes of dynamic warm-up. Avoid high-impact lunges due to the knee injury. Focus on pool-based cardio, resistance band drills, and hamstring stretches. Add vitamin-rich meals and hydration during peak hours."
        Also provide a simple weekly training/nutrition schedule in tabular format.
        """

    try:
        response = model.generate_content(
            [prompt],
            generation_config=genai.GenerationConfig(
                max_output_tokens=200,  # keep output short
                temperature=0.6
            )
        )

        st.subheader("🏆 Your Personalized Plan")

        # Format into shorter paragraphs
        formatted_text = "\n\n".join(
            textwrap.fill(p, width=80) for p in response.text.split("\n") if p.strip()
        )
        st.write(formatted_text)

        # --- Use pandas: create a simple weekly plan table ---
        weekly_plan = {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Workout": ["Cardio", "Strength", "Rest", "Agility", "Strength", "Cardio", "Rest"],
            "Nutrition Focus": ["High protein", "Balanced", "Hydration", "Carbs", "Protein", "Vitamins", "Hydration"]
        }
        df = pd.DataFrame(weekly_plan)
        st.write("📅 Example Weekly Plan:")
        st.dataframe(df)

        # --- Use matplotlib: bar chart of workout frequency ---
        workout_counts = df["Workout"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(workout_counts.index, workout_counts.values, color="skyblue")
        ax.set_ylabel("Frequency")
        ax.set_title("Workout Distribution")
        st.pyplot(fig)

        # --- Use plotly: pie chart of nutrition focus ---
        fig2 = px.pie(df, names="Nutrition Focus", title="Nutrition Focus Distribution")
        st.plotly_chart(fig2)

        # --- Use requests: motivational quote ---
        try:
            quote_api = "https://api.quotable.io/random?tags=motivational"
            r = requests.get(quote_api, timeout=5)
            if r.status_code == 200:
                quote = r.json().get("content", "")
                st.success(f"💡 Motivational Quote: {quote}")
        except Exception:
            st.warning("Could not fetch motivational quote.")

        # --- Evaluation & Analysis Section ---
        st.subheader("📊 Evaluation & Analysis")
        st.write("""
        **Cross-check with sport science:**  
        Compare warm-up and recovery suggestions with trusted sources like ACSM or ExRx.net.  
        Dynamic warm-ups and resistance bands are widely recommended for youth athletes.

        **Share with coaches/teachers:**  
        Present this plan to a PE teacher or coach. They can confirm whether the drills match the athlete’s age and position demands.

        **Refine prompts:**  
        If the output is too generic, add more detail (e.g., "female midfielder, age 14, preparing for a school tournament, with mild knee strain").  
        This helps Gemini tailor the advice more accurately.
        """)

    except Exception as e:
        st.error(f"Gemini API error: {e}")
