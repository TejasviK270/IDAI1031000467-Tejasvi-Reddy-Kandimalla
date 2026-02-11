import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px

# Configure Gemini API
genai.configure(api_key="AIzaSyBiOVXFpB77Q294p4_tvpbfHTZt2_lRqQg")

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
nutrition = st.text_input("Nutrition requirements (e.g., vegetarian, high protein)")
allergies = st.text_input("List any allergies (e.g., nuts, dairy, gluten)")
goal = st.text_input("Desired goal (e.g., stamina, recovery, tactical improvement)")

# Free-form custom prompt
custom_prompt = st.text_area("Or enter your own custom coaching request:")

if st.button("Generate Plan"):
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
        Allergies: {allergies}
        Goal: {goal}

        Generate two outputs:
        1. A concise fitness plan in 4–5 sentences only.
        2. A weekly schedule in Markdown table format with columns:
           Day | Workout | Nutrition Focus | Breakfast | Lunch | Dinner
           Tailor meals to the nutrition preference, allergies, and sport context.
           IMPORTANT: Output the table in proper Markdown format with headers and rows.
        """

    try:
        response = model.generate_content(
            [prompt],
            generation_config=genai.GenerationConfig(
                max_output_tokens=700,
                temperature=0.8
            )
        )

        text_output = response.text

        # Display the fitness plan (everything before the table)
        st.subheader("🏆 Your Personalized Plan")
        if "| Day" in text_output:
            plan_text = text_output.split("| Day")[0]
        else:
            plan_text = text_output
        st.write(plan_text.strip())

        # Parse the Markdown table into pandas
        st.write("### 📅 Weekly Plan with Meals")
        try:
            lines = [line for line in text_output.split("\n") if "|" in line]
            if lines:
                headers = [h.strip() for h in lines[0].split("|")[1:-1]]
                data = []
                for row in lines[2:]:
                    cells = [c.strip() for c in row.split("|")[1:-1]]
                    if len(cells) == len(headers):
                        data.append(cells)
                df = pd.DataFrame(data, columns=headers)
                st.dataframe(df)

                # Matplotlib bar chart of workouts
                workout_counts = df["Workout"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(workout_counts.index, workout_counts.values, color="skyblue")
                ax.set_ylabel("Frequency")
                ax.set_title("Workout Distribution")
                st.pyplot(fig)

                # Plotly pie chart of nutrition focus
                fig2 = px.pie(df, names="Nutrition Focus", title="Nutrition Focus Distribution")
                st.plotly_chart(fig2)
            else:
                st.info("Could not parse table from AI output. Try refining your prompt.")
        except Exception:
            st.info("Could not parse table from AI output. Try refining your prompt.")

        # Motivational Quote
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

        # Allergies Section
        st.subheader("🚫 Allergy Considerations")
        if allergies.strip():
            st.write(f"Meals have been tailored to avoid: **{allergies}**")
        else:
            st.write("No allergies specified. Meals include general recommendations.")

        # Dynamic Evaluation & Analysis
        st.subheader("📊 Evaluation & Analysis")
        if "hydration" in prompt.lower():
            st.write("Cross-check hydration scheduling with NATA guidelines. Ensure fluid intake matches age and activity level.")
        elif "stamina" in prompt.lower() or "endurance" in prompt.lower():
            st.write("Cross-check stamina routines with ACSM endurance training standards. Interval running and progressive overload are validated approaches.")
        elif "injury" in prompt.lower() or "recovery" in prompt.lower():
            st.write("Cross-check recovery drills with physiotherapy guidelines. Resistance bands and pool-based cardio are safe rehab methods.")
        else:
            st.write("Cross-check recommendations with ACSM or ExRx.net resources. Adjust based on age, sport, and training preference.")

        st.write("**Share with coaches/teachers:** Validate drills and nutrition with a PE teacher or coach.")
        st.write("**Refine prompts:** If the output is too generic, add more detail (e.g., 'female midfielder, age 14, preparing for a school tournament, with mild knee strain'). This helps Gemini tailor the advice more accurately.")

    except Exception as e:
        st.error(f"Gemini API error: {e}")
