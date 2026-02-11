import streamlit as st
import google.generativeai as genai
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import textwrap

# Configure Gemini API
genai.configure(api_key="AIzaSyDB9wFirBoOWOJCjstVxVEXXROgFtyfr-I")

# Try to load the best available model
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
    # Build the structured default prompt if no custom prompt is given
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

        Generate a personalized fitness plan including:
        - Workout routine
        - Recovery tips
        - Tactical advice
        - Nutrition guidance
        Keep the response concise, in short paragraphs.
        """

    try:
        response = model.generate_content([prompt])
        st.subheader("🏆 Your Personalized Plan")

        # Format response into shorter paragraphs
        formatted_text = "\n\n".join(
            textwrap.fill(p, width=80) for p in response.text.split("\n") if p.strip()
        )
        st.write(formatted_text)

        # --- Example use of pandas: store response in a DataFrame ---
        df = pd.DataFrame({"Prompt": [prompt], "Response": [response.text]})
        st.write("📊 Response stored in DataFrame:")
        st.dataframe(df)

        # --- Example use of matplotlib: simple bar chart of word counts ---
        word_count = len(response.text.split())
        fig, ax = plt.subplots()
        ax.bar(["Response Length"], [word_count], color="skyblue")
        ax.set_ylabel("Word Count")
        st.pyplot(fig)

        # --- Example use of plotly: interactive pie chart of sections ---
        sections = ["Workout", "Recovery", "Tactical", "Nutrition"]
        values = [response.text.lower().count(s.lower()) for s in sections]
        fig2 = px.pie(names=sections, values=values, title="Response Section Emphasis")
        st.plotly_chart(fig2)

        # --- Example use of requests: fetch a motivational quote ---
        try:
            quote_api = "https://api.quotable.io/random?tags=motivational"
            r = requests.get(quote_api, timeout=5)
            if r.status_code == 200:
                quote = r.json().get("content", "")
                st.success(f"💡 Motivational Quote: {quote}")
        except Exception:
            st.warning("Could not fetch motivational quote.")

    except Exception as e:
        st.error(f"Gemini API error: {e}")
