import streamlit as st
import pandas as pd
import joblib
import re
import os

import sklearn.tree

# 🔧 Fix missing attribute error (temporary but easy)
if not hasattr(sklearn.tree.DecisionTreeClassifier, "monotonic_cst"):
    sklearn.tree.DecisionTreeClassifier.monotonic_cst = None


# --- Load trained model ---
model_path = "model/model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("❌ Model file not found. Make sure 'model/model.pkl' exists.")
    st.stop()

# --- App Title ---
st.title("🔍 Phishing URL Detection App")
st.write("Enter a URL to check if it’s **Safe** or **Phishing** using a trained machine learning model.")

# --- Feature Extraction Function ---
def extract_features(url):
    features = {}

    features['Have_IP'] = 1 if re.search(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', url) else 0
    features['Have_At'] = 1 if '@' in url else 0
    features['URL_Length'] = len(url)
    features['URL_Depth'] = url.count('/')
    features['Redirection'] = 1 if url.count('//') > 1 else 0
    features['https_Domain'] = 1 if 'https' in url[8:] else 0
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|tinyurl|tr\.im|is\.gd|cli\.gs"
    features['TinyURL'] = 1 if re.search(shortening_services, url) else 0
    features['Prefix/Suffix'] = 1 if '-' in url else 0
    features['DNS_Record'] = 1
    features['Web_Traffic'] = 1
    features['Domain_Age'] = 12
    features['Domain_End'] = 6
    features['iFrame'] = 1 if "iframe" in url.lower() else 0
    features['Mouse_Over'] = 0
    features['Right_Click'] = 0
    features['Web_Forwards'] = 1 if url.count('//') > 2 else 0

    return pd.DataFrame([features])

# --- Streamlit UI ---
url = st.text_input("Enter a URL:")

if st.button("Predict"):
    if url:
        input_features = extract_features(url)
        prediction = model.predict(input_features)[0]

        if prediction == 1:
            st.error(f"🔴 Phishing URL detected: {url}")
        else:
            st.success(f"🟢 Safe URL: {url}")

        # Optional: show extracted features
      #  st.subheader("🔍 Extracted Features")
      #  st.dataframe(input_features)
    else:
        st.warning("Please enter a URL to check.")

# --- 💬 Feedback Section ---
st.markdown("---")
st.subheader("💬 Share Your Feedback")
st.write("We’d love to hear from you! Tell us what you think about this Phishing URL Detector.")

# Embed your Google Form link here 👇
st.markdown("[👉 Click here to fill out the feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeeW_J3U_xrOnBXnoQvSQFCoBw7o74LvffmJ1VW33leHEy5GQ/viewform?usp=publish-editor)", unsafe_allow_html=True)
