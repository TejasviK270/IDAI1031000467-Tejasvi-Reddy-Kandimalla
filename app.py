import streamlit as st
import google.generativeai as genai
import textwrap
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configure Gemini API
genai.configure(api_key="AIzaSyDB9wFirBoOWOJCjstVxVEXXROgFtyfr-I")

# Load model with fallback
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")
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
        """

    try:
        response = model.generate_content(
            [prompt],
            generation_config=genai.GenerationConfig(
                max_output_tokens=150,
                temperature=0.6
            )
        )

        st.subheader("🏆 Your Personalized Plan")

        # Format into shorter paragraphs
        formatted_text = "\n\n".join(
            textwrap.fill(p, width=80) for p in response.text.split("\n") if p.strip()
        )
        st.write(formatted_text)

        # --- Motivational Quote (requests library) ---
        try:
            quote_api = "https://api.quotable.io/random?tags=inspirational|sports|success"
            r = requests.get(quote_api, timeout=5)
            if r.status_code == 200 and "content" in r.json():
                quote = r.json().get("content", "")
                st.success(f"💡 Motivational Quote: {quote}")
            else:
                st.info("💡 Stay motivated: Believe in your training and trust the process!")
        except Exception:
            st.info("💡 Stay motivated: Believe in your training and trust the process!")

        # --- Example Weekly Plan (pandas + charts) ---
        weekly_plan = {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Workout": ["Cardio", "Strength", "Rest", "Agility", "Strength", "Cardio", "Rest"],
            "Nutrition Focus": ["High protein", "Balanced", "Hydration", "Carbs", "Protein", "Vitamins", "Hydration"]
        }
        df = pd.DataFrame(weekly_plan)
        st.write("📅 Example Weekly Plan:")
        st.dataframe(df)

        # Matplotlib bar chart
        workout_counts = df["Workout"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(workout_counts.index, workout_counts.values, color="skyblue")
        ax.set_ylabel("Frequency")
        ax.set_title("Workout Distribution")
        st.pyplot(fig)

        # Plotly pie chart
        fig2 = px.pie(df, names="Nutrition Focus", title="Nutrition Focus Distribution")
        st.plotly_chart(fig2)

        # --- Dynamic Evaluation & Analysis Section ---
        st.subheader("📊 Evaluation & Analysis")

        if "hydration" in prompt.lower():
            st.write("""
            **Cross-check with sport science:**  
            Compare hydration scheduling with guidelines from the National Athletic Trainers’ Association.  
            Ensure fluid intake matches age and activity level.

            **Share with coaches/teachers:**  
            Confirm hydration breaks align with school tournament rules.

            **Refine prompts:**  
            If the output is too generic, add more detail (e.g., "female midfielder, age 14, playing in hot weather conditions").
            """)

        elif "stamina" in prompt.lower() or "endurance" in prompt.lower():
            st.write("""
            **Cross-check with sport science:**  
            Review stamina-building routines against ACSM endurance training recommendations.  
            Interval running and progressive overload are widely validated.

            **Share with coaches/teachers:**  
            Coaches can adjust intensity to match age and fitness level.

            **Refine prompts:**  
            Add specifics like "two-week stamina plan for a 14-year-old midfielder" to get more tailored advice.
            """)

        elif "injury" in prompt.lower() or "recovery" in prompt.lower():
            st.write("""
            **Cross-check with sport science:**  
            Validate recovery drills with physiotherapy guidelines.  
            Resistance bands and pool-based cardio are often recommended for safe rehab.

            **Share with coaches/teachers:**  
            Ensure exercises are cleared by a physiotherapist or PE teacher.

            **Refine prompts:**  
            Specify injury type (e.g., "mild knee strain") for more accurate recovery suggestions.
            """)

        else:
            st.write("""
            **Cross-check with sport science:**  
            Compare recommendations with ACSM or ExRx.net resources.  
            Adjust based on age, sport, and training preference.

            **Share with coaches/teachers:**  
            Validate drills and nutrition with a PE teacher or coach.

            **Refine prompts:**  
            If the output is too generic, add more detail (e.g., "female midfielder, age 14, preparing for a school tournament, with mild knee strain").  
            This helps Gemini tailor the advice more accurately.
            """)

    except Exception as e:
        st.error(f"Gemini API error: {e}")
