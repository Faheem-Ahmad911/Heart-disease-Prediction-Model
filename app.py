import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load the trained model
model = pickle.load(open('heart_disease_model.pkl', 'rb'))

# App title
st.title('Heart Disease Prediction Web App')

# User inputs
st.subheader('Enter Patient Data:')

age = st.number_input('Age', min_value=1, max_value=120, value=30)
sex = st.selectbox('Sex', options=['Male', 'Female'])
cp = st.selectbox('Chest Pain Type (cp)', options=[0, 1, 2, 3])
trestbps = st.number_input('Resting Blood Pressure (trestbps)', min_value=80, max_value=200, value=120)
chol = st.number_input('Serum Cholesterol (chol)', min_value=100, max_value=600, value=200)
fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl (fbs)', options=[0, 1])
restecg = st.selectbox('Resting Electrocardiographic Results (restecg)', options=[0, 1, 2])
thalach = st.number_input('Maximum Heart Rate Achieved (thalach)', min_value=60, max_value=220, value=150)
exang = st.selectbox('Exercise Induced Angina (exang)', options=[0, 1])
oldpeak = st.number_input('ST Depression Induced by Exercise (oldpeak)', min_value=0.0, max_value=6.0, value=1.0, step=0.1)
slope = st.selectbox('Slope of the Peak Exercise ST Segment (slope)', options=[0, 1, 2])
ca = st.selectbox('Number of Major Vessels Colored by Fluoroscopy (ca)', options=[0, 1, 2, 3, 4])
thal = st.selectbox('Thalassemia (thal)', options=[0, 1, 2, 3])

# Convert sex and other categorical variables if needed
sex = 1 if sex == 'Male' else 0

# Prediction
if st.button('Predict'):
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                            thalach, exang, oldpeak, slope, ca, thal]])
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error('High Risk of Heart Disease!')
    else:
        st.success('Low Risk of Heart Disease.')

