import streamlit as st
import numpy as np
import pickle
import math

# Configure page
st.set_page_config(page_title="IPL Score Predictor", layout="centered")
import joblib

model = joblib.load("ipl_score_model_compressed.joblib")

# Teams
teams = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
         'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
         'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

# Custom Styling
st.markdown("""
    <style>
        html, body, .stApp {
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            text-align: center;
            color: #2c3e50;
            font-size: 44px;
            font-weight: 900;
            margin-bottom: 10px;
        }
        .sub {
            text-align: center;
            color: #555;
            font-size: 20px;
            margin-bottom: 30px;
        }
        .stButton > button {
            background: linear-gradient(to right, #1abc9c, #16a085);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        }
        .stButton > button:hover {
            transform: scale(1.02);
            background: linear-gradient(to right, #16a085, #1abc9c);
        }
        .score-box {
            background: #ffffff;
            padding: 30px;
            text-align: center;
            font-size: 26px;
            color: #2c3e50;
            border-radius: 16px;
            font-weight: bold;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>🏏 IPL Score Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub'>Predict the first innings score based on match progress</h4>", unsafe_allow_html=True)

# Description
with st.expander("📘 Description"):
    st.info("""
        This ML model predicts the final score of the **first innings** in an IPL match based on current match data.  
        📌 Ensure at least **5 overs** are completed for accurate predictions.
    """)

# --- TEAM SELECTION ---
st.subheader("🧢 Team Selection")
batting_team = st.selectbox("🏏 Batting Team", teams)
bowling_team = st.selectbox("🎯 Bowling Team", [team for team in teams if team != batting_team])

# Encode teams
prediction_array = [1 if team == batting_team else 0 for team in teams]
prediction_array += [1 if team == bowling_team else 0 for team in teams]

# --- MATCH INPUTS ---
st.subheader("📊 Match Inputs")

col1, col2 = st.columns(2)
with col1:
    overs = st.number_input("Overs Completed", min_value=5.0, max_value=20.0, step=0.1)
    if overs - math.floor(overs) > 0.5:
        st.error("⚠️ Invalid input — 1 over has only 6 balls")

with col2:
    runs = st.number_input("Current Runs", min_value=0, max_value=300)

wickets = st.slider("Wickets Fallen", 0, 9)

col3, col4 = st.columns(2)
with col3:
    runs_in_prev_5 = st.number_input("Runs in Last 5 Overs", min_value=0, max_value=runs)
with col4:
    wickets_in_prev_5 = st.number_input("Wickets in Last 5 Overs", min_value=0, max_value=wickets)

# --- PREDICTION ---
st.subheader("🔮 Prediction")
if st.button("Predict Score"):
    prediction_array += [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]
    prediction_array = np.array([prediction_array])
    predicted_score = int(round(model.predict(prediction_array)[0]))

    st.markdown(f"""
        <div class="score-box">
            🎯 <strong>Predicted Final Score</strong><br><br>
            {predicted_score - 5} <strong>to</strong> {predicted_score + 5} <strong>Runs</strong>
        </div>
    """, unsafe_allow_html=True)
