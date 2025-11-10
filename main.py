import streamlit as st
from prediction_helper import predict

# Page configuration
st.set_page_config(
    page_title="Health Insurance Cost Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 4rem 3rem;
        margin-bottom: 3rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeIn 0.8s ease-out;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
        animation: slideInLeft 0.8s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
        line-height: 1.6;
        position: relative;
        z-index: 1;
        max-width: 600px;
        animation: slideInLeft 1s ease-out;
    }
    
    /* Stats Cards */
    .stats-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: fadeInUp 0.8s ease-out;
        animation-fill-mode: both;
    }
    
    .stats-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
        background: rgba(255, 255, 255, 1);
    }
    
    .stats-number {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        color: #718096;
        font-weight: 600;
    }
    
    /* Glassmorphism Form Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        padding: 3rem 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3748;
        margin: 2.5rem 0 1.5rem 0;
        padding-left: 1.25rem;
        border-left: 5px solid #667eea;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideInRight 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .section-header:hover {
        padding-left: 1.5rem;
        color: #667eea;
    }
    
    /* Labels - MEDIUM SIZE with perfect contrast */
    .stNumberInput > label,
    .stSelectbox > label {
        font-weight: 600 !important;
        color: #1a202c !important;
        font-size: 1rem !important;
        margin-bottom: 0.65rem !important;
        display: block !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    /* Input spacing */
    .stNumberInput,
    .stSelectbox {
        margin-bottom: 1.75rem;
    }
    
    /* CONSISTENT Number Input Styling */
    .stNumberInput > div > div > input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #2d3748 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #667eea !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 4px 16px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-2px) !important;
        outline: none !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* CONSISTENT Select Box Styling */
    .stSelectbox > div > div {
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 4px 16px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stSelectbox select {
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #2d3748 !important;
        background: transparent !important;
    }
    
    /* Number input buttons with hover */
    .stNumberInput button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        width: 36px !important;
        height: 36px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stNumberInput button:hover {
        transform: scale(1.15) rotate(5deg) !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stNumberInput button:active {
        transform: scale(0.95) !important;
    }
    
    /* Primary Button with enhanced hover */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1.2rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        text-transform: none !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Result Card with fade effect */
    .result-card {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.95) 0%, rgba(56, 239, 125, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 45px rgba(17, 153, 142, 0.35);
        animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .result-label {
        font-size: 1.2rem;
        font-weight: 600;
        opacity: 0.95;
        margin-bottom: 1rem;
        animation: fadeIn 0.8s ease-out 0.2s both;
    }
    
    .result-amount {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        animation: fadeIn 0.8s ease-out 0.4s both;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .result-note {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 1rem;
        animation: fadeIn 0.8s ease-out 0.6s both;
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 0.85rem;
    }
    
    /* Enhanced Tooltip with hover */
    [data-testid="stTooltipIcon"] {
        color: #667eea !important;
        opacity: 0.6;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    [data-testid="stTooltipIcon"]:hover {
        opacity: 1;
        transform: scale(1.3) rotate(15deg);
        color: #764ba2 !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    /* Stagger animation for stats cards */
    .stats-card:nth-child(1) { animation-delay: 0.1s; }
    .stats-card:nth-child(2) { animation-delay: 0.2s; }
    .stats-card:nth-child(3) { animation-delay: 0.3s; }
    .stats-card:nth-child(4) { animation-delay: 0.4s; }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .footer-text {
        color: #718096;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .footer-highlight {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        .hero-title {
            font-size: 3rem;
        }
        
        .stats-number {
            font-size: 2.3rem;
        }
    }
    
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .hero-section {
            padding: 3rem 2rem;
        }
        
        .hero-title {
            font-size: 2.2rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .glass-container {
            padding: 2rem 1.5rem;
        }
        
        [data-testid="column"] {
            padding: 0 0.5rem;
        }
        
        .stats-number {
            font-size: 2rem;
        }
        
        .result-amount {
            font-size: 2.5rem;
        }
        
        .section-header {
            font-size: 1.1rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.8rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .stats-card {
            padding: 1.5rem 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Protect What Matters Most</div>
        <div class="hero-subtitle">Get accurate health insurance cost predictions powered by advanced AI. Make informed decisions for you and your family.</div>
    </div>
""", unsafe_allow_html=True)

# Stats Section
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="stats-card">
            <div class="stats-number">98%</div>
            <div class="stats-label">Accuracy</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="stats-card">
            <div class="stats-number">50K+</div>
            <div class="stats-label">Predictions</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="stats-card">
            <div class="stats-number">4.9★</div>
            <div class="stats-label">Rating</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="stats-card">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Support</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

# Glassmorphism Form Container
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Section 1: Personal Information
st.markdown('<p class="section-header">👤 Personal Information</p>', unsafe_allow_html=True)
row1 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=18, help="Your current age")
    
with row1[1]:
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20, value=0, help="Family members dependent on you")
    
with row1[2]:
    income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200, value=0, help="Annual income (₹ Lakhs)")

# Section 2: Insurance Details
st.markdown('<p class="section-header">🛡️ Insurance & Employment</p>', unsafe_allow_html=True)
row2 = st.columns(3)

with row2[0]:
    genetical_risk = st.number_input('Genetical Risk', step=1, min_value=0, max_value=5, value=0, help="Risk score (0-5)")
    
with row2[1]:
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'], help="Coverage tier")
    
with row2[2]:
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'], help="Work status")

# Section 3: Demographics
st.markdown('<p class="section-header">📋 Demographics</p>', unsafe_allow_html=True)
row3 = st.columns(3)

with row3[0]:
    gender = st.selectbox('Gender', categorical_options['Gender'])
    
with row3[1]:
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
    
with row3[2]:
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'], help="Body Mass Index")

# Section 4: Health & Location
st.markdown('<p class="section-header">🏥 Health & Location</p>', unsafe_allow_html=True)
row4 = st.columns(3)

with row4[0]:
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
    
with row4[1]:
    region = st.selectbox('Region', categorical_options['Region'], help="Residential area")
    
with row4[2]:
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'], help="Existing conditions")

# Create input dictionary
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# Button
st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('Get Your Insurance Quote'):
        with st.spinner('🔄 Analyzing your information...'):
            prediction = predict(input_dict)
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Your Estimated Health Insurance Cost</div>
                    <div class="result-amount">₹{prediction}</div>
                    <div class="result-note">✓ Calculated using AI-powered analysis</div>
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p class="footer-text">
            <span class="footer-highlight">💡 Smart Predictions</span> • All estimates are based on advanced machine learning models<br>
            Results may vary based on additional factors • For informational purposes only<br><br>
            <span style="font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Made with ❤️ for better insurance decisions</span>
        </p>
    </div>
""", unsafe_allow_html=True)









###########################################################################
# import streamlit as st
# from prediction_helper import predict

# # Define the page layout
# st.title('Health Insurance Cost Predictor')

# categorical_options = {
#     'Gender': ['Male', 'Female'],
#     'Marital Status': ['Unmarried', 'Married'],
#     'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
#     'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
#     'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
#     'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
#     'Medical History': [
#         'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
#         'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
#         'Diabetes & Heart disease'
#     ],
#     'Insurance Plan': ['Bronze', 'Silver', 'Gold']
# }

# # Create four rows of three columns each
# row1 = st.columns(3)
# row2 = st.columns(3)
# row3 = st.columns(3)
# row4 = st.columns(3)

# # Assign inputs to the grid
# with row1[0]:
#     age = st.number_input('Age', min_value=18, step=1, max_value=100)
# with row1[1]:
#     number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20)
# with row1[2]:
#     income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)

# with row2[0]:
#     genetical_risk = st.number_input('Genetical Risk', step=1, min_value=0, max_value=5)
# with row2[1]:
#     insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
# with row2[2]:
#     employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])

# with row3[0]:
#     gender = st.selectbox('Gender', categorical_options['Gender'])
# with row3[1]:
#     marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
# with row3[2]:
#     bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

# with row4[0]:
#     smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
# with row4[1]:
#     region = st.selectbox('Region', categorical_options['Region'])
# with row4[2]:
#     medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

# # Create a dictionary for input values
# input_dict = {
#     'Age': age,
#     'Number of Dependants': number_of_dependants,
#     'Income in Lakhs': income_lakhs,
#     'Genetical Risk': genetical_risk,
#     'Insurance Plan': insurance_plan,
#     'Employment Status': employment_status,
#     'Gender': gender,
#     'Marital Status': marital_status,
#     'BMI Category': bmi_category,
#     'Smoking Status': smoking_status,
#     'Region': region,
#     'Medical History': medical_history
# }

# # Button to make prediction
# if st.button('Predict'):
#     prediction = predict(input_dict)
#     st.success(f'Predicted Health Insurance Cost: {prediction}')
