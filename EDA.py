import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def render():
    st.title("📊 Exploratory Data Analysis (EDA)")

    st.write("This section provides interactive data visualizations, tables, and statistical insights from the Heart Disease dataset. Use the features below to explore trends, distributions, and potential relationships in the data.")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("🔍 Dataset Preview")
        st.write(df.head())

        st.subheader("📈 Summary Statistics")
        st.write(df.describe())

        st.subheader("🧮 Null Value Count")
        st.write(df.isnull().sum())

        # Column selection
        st.subheader("📌 Column Selection")
        selected_column = st.selectbox("Select a column for distribution plot", df.columns)

        if df[selected_column].dtype in ['int64', 'float64']:
            st.subheader(f"📊 Distribution of '{selected_column}'")
            fig, ax = plt.subplots()
            sns.histplot(df[selected_column], kde=True, ax=ax)
            st.pyplot(fig)

        # Correlation heatmap
        st.subheader("🔗 Correlation Matrix")
        if df.select_dtypes(include=['int64', 'float64']).shape[1] >= 2:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax2)
            st.pyplot(fig2)

        st.success("✅ EDA completed. Scroll above to explore the insights.")
    else:
        st.info("Please upload a CSV file to begin EDA.")
