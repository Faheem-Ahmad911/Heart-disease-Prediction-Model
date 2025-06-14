import streamlit as st
import pandas as pd
import os
from datetime import datetime
import EDA as eda_page
import Model as model_page

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction App", 
    page_icon="❤️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"  # "login" or "signup"

# Excel file path - Update this to your Excel file path
EXCEL_FILE_PATH = "users.xlsx"  # Change this to your actual Excel file path

def load_user_data():
    """Load user data from Excel file"""
    try:
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)
            # Ensure the required columns exist
            if 'FullName' not in df.columns or 'Email' not in df.columns:
                # Create default structure if columns don't exist
                df = pd.DataFrame(columns=['FullName', 'Email', 'SignupDate'])
                df.to_excel(EXCEL_FILE_PATH, index=False)
            return df
        else:
            # Create new Excel file if it doesn't exist
            df = pd.DataFrame(columns=['FullName', 'Email', 'SignupDate'])
            df.to_excel(EXCEL_FILE_PATH, index=False)
            return df
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        return pd.DataFrame(columns=['FullName', 'Email', 'SignupDate'])

def save_user_data(df):
    """Save user data to Excel file"""
    try:
        df.to_excel(EXCEL_FILE_PATH, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving user data: {str(e)}")
        return False

def verify_user(email, name):
    """Verify if user exists in Excel file"""
    df = load_user_data()
    if not df.empty:
        # Check if email exists and name matches
        user_row = df[df['Email'].str.lower() == email.lower()]
        if not user_row.empty:
            stored_name = user_row.iloc[0]['FullName']
            if stored_name.lower().strip() == name.lower().strip():
                return True, "User verified successfully"
            else:
                return False, "Name doesn't match our records"
        else:
            return False, "Email not found in our records"
    return False, "No user data found"

def add_new_user(name, email):
    """Add new user to Excel file"""
    df = load_user_data()
    
    # Check if email already exists
    if not df.empty and email.lower() in df['Email'].str.lower().values:
        return False, "Email already exists! Please use login instead."
    
    # Add new user
    new_user = pd.DataFrame({
        'FullName': [name],
        'Email': [email],
        'SignupDate': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    
    df = pd.concat([df, new_user], ignore_index=True)
    
    if save_user_data(df):
        return True, "Account created successfully! You can now login."
    else:
        return False, "Error creating account. Please try again."

def auth_page():
    # Custom CSS for authentication page
    st.markdown("""
    <style>
        .auth-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 85vh;
        }
        
        .auth-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            color: white;
            max-width: 500px;
            width: 100%;
        }
        
        .auth-header {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .auth-subtitle {
            font-size: 1.1rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .heart-pulse {
            font-size: 4rem;
            animation: pulse 2s infinite;
            margin-bottom: 20px;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            padding: 15px;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FFD700;
            box-shadow: 0 0 10px rgba(255,215,0,0.3);
        }
        
        .stTextInput > label {
            color: white !important;
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .mode-switch {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .mode-button {
            background: rgba(255,255,255,0.1);
            color: white;
            border: 2px solid rgba(255,255,255,0.2);
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .mode-button.active {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: #333;
            border-color: #FFD700;
        }
        
        .mode-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255,215,0,0.3);
        }
        
        .features-preview {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-top: 30px;
            backdrop-filter: blur(10px);
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            margin: 10px 0;
            font-size: 1rem;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            margin-right: 15px;
        }
        
        .background-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .info-section {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 0.9rem;
        }
        
        .excel-info {
            background: rgba(255,215,0,0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,215,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated background
    st.markdown('<div class="background-animation"></div>', unsafe_allow_html=True)
    
    # Main auth container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        with st.container():
            # Heart icon with animation
            st.markdown('<div class="heart-pulse">❤️</div>', unsafe_allow_html=True)
            
            # Header
            st.markdown('<h1 class="auth-header">HeartCare AI</h1>', unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">Advanced Heart Disease Prediction Platform</p>', unsafe_allow_html=True)
            

            
            # Mode Selection Buttons
            col_login, col_signup = st.columns(2)
            
            with col_login:
                if st.button("🔐 Login", key="login_mode", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            with col_signup:
                if st.button("📝 Sign Up", key="signup_mode", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
            
            # Show current mode
            if st.session_state.auth_mode == "login":
                st.markdown("### 🔐 Login to Your Account")
                st.markdown("Enter your credentials to access the application")
            else:
                st.markdown("### 📝 Create New Account")
                st.markdown("Register to get access to our AI-powered heart disease prediction")
            
            # Authentication Form
            with st.form("auth_form", clear_on_submit=False):
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email Address", placeholder="Enter your email address")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                
                with col_btn2:
                    if st.session_state.auth_mode == "login":
                        submitted = st.form_submit_button("🚀 Login", use_container_width=True)
                    else:
                        submitted = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if submitted:
                    if name and email:
                        if "@" in email and "." in email:
                            if st.session_state.auth_mode == "login":
                                # Login Process
                                success, message = verify_user(email, name)
                                if success:
                                    st.session_state.logged_in = True
                                    st.session_state.user_name = name
                                    st.session_state.user_email = email
                                    st.success("✅ Login Successful! Welcome back!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                                    if "not found" in message.lower():
                                        st.info("💡 Email not found? Try creating a new account!")
                            else:
                                # Signup Process
                                success, message = add_new_user(name, email)
                                if success:
                                    st.success(f"✅ {message}")
                                    st.info("🔄 Please switch to Login mode to access your account")
                                    st.session_state.auth_mode = "login"
                                else:
                                    st.error(f"❌ {message}")
                        else:
                            st.error("❌ Please enter a valid email address")
                    else:
                        st.error("❌ Please fill in all fields")
            
            # Mode-specific information
            if st.session_state.auth_mode == "login":
                st.markdown("""
                <div class="info-section">
                    <h4>🔍 Login Instructions:</h4>
                    <ul>
                        <li>Enter your <strong>exact full name</strong> as registered</li>
                        <li>Use the <strong>same email address</strong> from your account</li>
                        <li>Names and emails are case-insensitive</li>
                        <li>If you're new, click <strong>"Sign Up"</strong> to create an account</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-section">
                    <h4>📝 Sign Up Instructions:</h4>
                    <ul>
                        <li>Enter your <strong>full name</strong> (this will be stored)</li>
                        <li>Provide a <strong>valid email address</strong></li>
                        <li>Email must be unique (not already registered)</li>
                        <li>After signup, switch to <strong>"Login"</strong> to access the app</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Features preview
            st.markdown("""
            <div class="features-preview">
                <h3 style="margin-bottom: 20px;">🌟 What You'll Access:</h3>
                <div class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span>Interactive Data Exploration & Visualizations</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🤖</span>
                    <span>AI-Powered Heart Disease Prediction</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📈</span>
                    <span>Real-time Risk Assessment & Analytics</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🩺</span>
                    <span>Clinical Insights & Recommendations</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Current users count (if Excel file exists)
            try:
                df = load_user_data()
                if not df.empty:
                    user_count = len(df)
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: 20px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                        <strong>👥 Registered Users: {user_count}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        st.markdown('</div>', unsafe_allow_html=True)

def main_app():
    # Custom CSS for main app
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        
        .user-welcome {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .stats-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 5px;
        }
        
        .goal-section {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            margin: 20px 0;
        }
        
        .heart-icon {
            font-size: 4rem;
            color: #FF6B6B;
            text-align: center;
            animation: heartbeat 1.5s ease-in-out infinite;
        }
        
        @keyframes heartbeat {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # User welcome section
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div class="user-welcome">
            <h3>👋 Welcome back, {st.session_state.user_name}!</h3>
            <p>📧 {st.session_state.user_email}</p>
            
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Header Section
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.markdown('<div class="heart-icon">❤️</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">Heart Disease Prediction</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Advanced ML-Powered Cardiovascular Risk Assessment</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Enhanced Sidebar Navigation
    st.sidebar.markdown(f"### 👤 User: {st.session_state.user_name}")
    st.sidebar.markdown(f"📧 {st.session_state.user_email}")
    
    if st.sidebar.button("🚪 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.session_state.auth_mode = "login"
        st.success("👋 Logged out successfully!")
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    menu = st.sidebar.radio(
        "",
        ["🏠 Home", "📊 EDA", "🤖 Model"],
        format_func=lambda x: x.split(" ", 1)[1]
    )

    # Sidebar additional info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Quick Stats")
    st.sidebar.metric("Dataset Size", "3030 patients")
    st.sidebar.metric("Features", "13 attributes")
    st.sidebar.metric("Accuracy Target", "> 85%")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Resources")
    st.sidebar.markdown("[UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)")
    st.sidebar.markdown("[Documentation](https://docs.streamlit.io)")

    # Show current Excel file users count
    try:
        df = load_user_data()
        if not df.empty:
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"### 👥 Total Users: {len(df)}")
    except:
        pass

    # Page Control
    if menu == '🏠 Home':
        # Hero Section
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
                <h2>🩺 Predict Heart Disease with AI</h2>
                <p>Leverage machine learning to assess cardiovascular risk using clinical parameters</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature Cards Section
        st.markdown("## ✨ Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>📊 Interactive EDA</h3>
                <p>Explore comprehensive data visualizations and statistical insights</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 ML Models</h3>
                <p>Multiple algorithms trained and optimized for best performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>⚡ Real-time Prediction</h3>
                <p>Instant risk assessment with confidence intervals</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Rest of the home page content...
        st.markdown("## 📋 Dataset Overview")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("### 📊 Dataset Statistics")
            
            stats_col1, stats_col2 = st.columns(2)
            
            with stats_col1:
                st.markdown("""
                <div class="stats-card">
                    <h3>3030</h3>
                    <p>Total Patients</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="stats-card">
                    <h3>13</h3>
                    <p>Features</p>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_col2:
                st.markdown("""
                <div class="stats-card">
                    <h3>UCI</h3>
                    <p>Data Source</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="stats-card">
                    <h3>Binary</h3>
                    <p>Classification</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🔍 Key Attributes")
            
            features = [
                "👤 Age & Gender", "💓 Chest Pain Type", 
                "🩸 Blood Pressure", "🧪 Cholesterol Levels",
                "📈 Max Heart Rate", "⚡ Exercise Induced Angina",
                "📊 ST Depression", "🔬 ECG Results"
            ]
            
            for i in range(0, len(features), 2):
                fcol1, fcol2 = st.columns(2)
                with fcol1:
                    if i < len(features):
                        st.markdown(f"• {features[i]}")
                with fcol2:
                    if i + 1 < len(features):
                        st.markdown(f"• {features[i + 1]}")

    elif menu == '📊 EDA':
        eda_page.render()

    elif menu == '🤖 Model':
        model_page.render()

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; color: #666;">
        <p>💝 Built with Streamlit • ❤️ Powered by Machine Learning • 🩺 For Better Healthcare</p>
        
    </div>
    """, unsafe_allow_html=True)

# Main app logic
if st.session_state.logged_in:
    main_app()
else:
    auth_page()