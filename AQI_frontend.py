import streamlit as st
import pickle

# --- Page Configuration ---
st.set_page_config(
    page_title="Air Quality Predictor",
    page_icon="🍃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background: #f0f2f6; /* Light gray background */
    }

    .stApp {
        background: #f0f2f6;
    }

    /* Header Styling */
    .stApp header {
        background-color: #ffffff; /* White background for header */
        padding: 1rem 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* Soft shadow */
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .stApp header h1 {
        color: #2c3e50; /* Darker text for title */
        font-weight: 700;
        text-align: center;
        margin: 0;
        padding: 0;
    }
    .stApp header h2 {
        color: #7f8c8d; /* Subtitle color */
        font-weight: 400;
        text-align: center;
        margin-top: 0.5rem;
    }

    /* Main Container Styling */
    .st-emotion-cache-z5fcl4 { /* This targets the main content div, might need adjustment with Streamlit updates */
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 15px; /* Rounded corners */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* More pronounced soft shadow */
        margin-top: 2rem;
    }

    /* Input Fields Styling */
    .stNumberInput > label {
        font-weight: 600;
        color: #34495e;
        margin-bottom: 0.5rem;
    }
    .stNumberInput div[data-baseweb="input"] > div {
        border-radius: 8px;
        border: 1px solid #dcdcdc;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .stNumberInput div[data-baseweb="input"] > div:focus-within {
        border-color: #3498db; /* Blue on focus */
        box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    }

    /* Button Styling */
    .stButton > button {
        background-color: #3498db; /* Blue button */
        color: white;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease, transform 0.2s ease;
        width: 100%;
        margin-top: 1.5rem;
    }
    .stButton > button:hover {
        background-color: #2980b9; /* Darker blue on hover */
        transform: translateY(-2px);
    }

    /* Output/Prediction Section Styling */
    .stMarkdown h3 {
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    /* AQI Status Boxes */
    .aqi-status {
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        font-weight: 700;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .aqi-status:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
    }

    .aqi-good { background-color: #27ae60; } /* Emerald Green */
    .aqi-moderate { background-color: #f1c40f; color: #333;} /* Sunflower Yellow */
    .aqi-sensitive { background-color: #e67e22; } /* Carrot Orange */
    .aqi-unhealthy { background-color: #e74c3c; } /* Alizarin Red */
    .aqi-very-unhealthy { background-color: #8e44ad; } /* Amethyst */
    .aqi-hazardous { background-color: #c0392b; } /* Pomegranate */

    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #7f8c8d;
        font-size: 0.9em;
        border-top: 1px solid #e0e0e0;
    }
    .footer a {
        color: #3498db;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }

    /* Remove Streamlit default header/footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- Load Model (ensure your file path is correct) ---
try:
    with open(r"C:\Users\ASUS\Desktop\intship\finalmodel.pkl", "rb") as file:
        Regressor = pickle.load(file)
except FileNotFoundError:
    st.error("Error: 'finalmodel.pkl' not found. Please ensure the model file is in the correct directory.")
    st.stop() # Stop execution if model is not found

# --- Header Section ---
st.markdown("""
    <header>
        <h1>🍃 Air Quality Predictor</h1>
        <h2>Understand the air you breathe.</h2>
    </header>
""", unsafe_allow_html=True)

# --- Main Application Layout ---
st.write("### Enter the measure of gases:")

# Use columns for a grid-like input layout
col1, col2 = st.columns(2)

with col1:
    a = st.number_input("Carbon Monoxide (CO)", min_value=0.0, format="%.2f")
    c = st.number_input("Nitrogen Dioxide (NO2)", min_value=0.0, format="%.2f")
    e = st.number_input("Particulate Matter (PM2.5)", min_value=0.0, format="%.2f")

with col2:
    b = st.number_input("Ozone (O3)", min_value=0.0, format="%.2f")
    d = st.number_input("Sulfur Dioxide (SO2)", min_value=0.0, format="%.2f")
    f = st.number_input("Particulate Matter (PM10)", min_value=0.0, format="%.2f")

if st.button("Predict AQI"):
    if any(val is None for val in [a, b, c, d, e, f]):
        st.warning("Please enter values for all gas measurements.")
    else:
        result = Regressor.predict([[a, b, c, d, e, f]])
        aqi_value = round(result[0], 2) # Round to 2 decimal places for cleaner display

        st.markdown("---")
        st.markdown("### Prediction Results:")

        aqi_status_class = ""
        aqi_description = ""

        if aqi_value < 50:
            aqi_status_class = "aqi-good"
            aqi_description = "Good"
        elif 50 <= aqi_value < 100:
            aqi_status_class = "aqi-moderate"
            aqi_description = "Moderate"
        elif 100 <= aqi_value < 150:
            aqi_status_class = "aqi-sensitive"
            aqi_description = "Unhealthy for Sensitive Groups"
        elif 150 <= aqi_value < 200:
            aqi_status_class = "aqi-unhealthy"
            aqi_description = "Unhealthy"
        elif 200 <= aqi_value < 300:
            aqi_status_class = "aqi-very-unhealthy"
            aqi_description = "Very Unhealthy"
        else:
            aqi_status_class = "aqi-hazardous"
            aqi_description = "Hazardous"

        st.markdown(f"""
            <div class='aqi-status {aqi_status_class}'>
                <h2>Predicted AQI: {aqi_value}</h2>
                <p>Status: {aqi_description}</p>
            </div>
        """, unsafe_allow_html=True)

# --- Footer Section ---
st.markdown("""
    <div class="footer">
        <p>Designed with ❤️ </p>
        <p>Data provided for informational purposes only. Consult local authorities for official air quality data.</p>
    </div>
""", unsafe_allow_html=True)