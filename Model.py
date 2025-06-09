import streamlit as st
import numpy as np
import pickle
from fpdf import FPDF
from io import BytesIO
import os

# Load the trained model with error handling
@st.cache_resource
def load_model():
    try:
        if os.path.exists('heart_disease_model.pkl'):
            model = pickle.load(open('heart_disease_model.pkl', 'rb'))
            return model
        else:
            st.error("Model file 'heart_disease_model.pkl' not found!")
            return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def generate_pdf(data, prediction_text):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.cell(200, 10, txt="Heart Disease Prediction Report", ln=True, align='C')
        pdf.ln(10)

        # Patient details
        pdf.cell(200, 10, txt="Patient Details:", ln=True, align='L')
        pdf.ln(5)

        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')

        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Prediction Result: {prediction_text}", ln=True, align='L')

        # Get PDF content as bytes
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return pdf_output
    
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

def render():
    st.title("🤖 Heart Disease Prediction")
    st.write("Enter the patient data below to predict the likelihood of heart disease.")

    # Load model
    model = load_model()
    if model is None:
        st.stop()  # Stop execution if model can't be loaded

    st.subheader('Enter Patient Data:')

    # User inputs
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

    # Convert sex to numerical
    sex_num = 1 if sex == 'Male' else 0

    # Prediction button
    if st.button('Predict'):
        try:
            # Prepare input data
            input_data = np.array([[age, sex_num, cp, trestbps, chol, fbs, restecg,
                                    thalach, exang, oldpeak, slope, ca, thal]])
            
            # Make prediction
            prediction = model.predict(input_data)

            # Display result
            if prediction[0] == 1:
                st.error('⚠️ High Risk of Heart Disease!')
                prediction_text = "High Risk of Heart Disease"
            else:
                st.success('✅ Low Risk of Heart Disease.')
                prediction_text = "Low Risk of Heart Disease"

            # Collect data for PDF
            patient_data = {
                "Age": age,
                "Sex": sex,
                "Chest Pain Type": cp,
                "Resting Blood Pressure": trestbps,
                "Serum Cholesterol": chol,
                "Fasting Blood Sugar > 120 mg/dl": fbs,
                "Resting ECG": restecg,
                "Max Heart Rate Achieved": thalach,
                "Exercise Induced Angina": exang,
                "ST Depression": oldpeak,
                "Slope": slope,
                "Number of Major Vessels": ca,
                "Thalassemia": thal
            }

            # Generate PDF
            pdf_buffer = generate_pdf(patient_data, prediction_text)
            
            if pdf_buffer is not None:
                st.download_button(
                    label="📄 Download Report as PDF",
                    data=pdf_buffer,
                    file_name="Heart_Disease_Prediction_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate PDF report.")
                
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

# Call the render function if running as main
if __name__ == "__main__":
    render()