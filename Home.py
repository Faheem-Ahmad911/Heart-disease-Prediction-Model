import streamlit as st
import EDA as eda_page
import Model as model_page

# Page configuration
st.set_page_config(page_title="Heart Disease Prediction App", page_icon="❤️", layout="wide")

# Logo Section
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=80)
with col2:
    st.title("Heart Disease Prediction App")

st.markdown("---")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "EDA", "Model"]
)

# Page Control
if menu == 'Home':
    st.header("Project Overview")
    st.write("""
    Welcome to the Heart Disease Prediction App!  
    This project is designed to predict the likelihood of heart disease based on a set of medical parameters provided by the user.

    ### Dataset:
    - **Source:** UCI Machine Learning Repository
    - **Size:** 303 entries
    - **Features:** Age, Sex, Chest Pain Type, Resting Blood Pressure, Cholesterol, Fasting Blood Sugar, Rest ECG, Max Heart Rate, Exercise Induced Angina, ST Depression, and more.

    ### Project Goal:
    The goal of this project is to build a machine learning model that can accurately predict the presence of heart disease based on patient data.  
    This application allows users to:
    - Explore the dataset through interactive visualizations.
    - Understand the model building process.
    - Make real-time predictions using the trained model.
    """)

elif menu == 'EDA':
    eda_page.render()

elif menu == 'Model':
    model_page.render()
