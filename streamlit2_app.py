import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib
import os
!pip install catboost
import CatBoostClassifier


# Load the trained model with caching
@st.cache_resource
def load_model():
    try:
        return joblib.load("model_top5.pkl")  # Load the updated model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None
        
model = load_model()

def load_data():
    try:
        return pd.read_csv("df.csv") 
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Define only the top 5 features
REQUIRED_COLUMNS = [
    "year_month_2024-08",  # One-hot encoded feature
    "total_visits",
    "avg_days_between_pickups",
    "days_since_last_pickup",
    "year_month_2024-06"
]

# Function to preprocess input data
def preprocess_input(input_data):
    input_df = pd.DataFrame([input_data])

    # Ensure all required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in input_df.columns:
            input_df[col] = 0  # Set missing columns to 0

    # Ensure the column order matches model training
    input_df = input_df[REQUIRED_COLUMNS]
    return input_df

# Set the background image (optional)
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def powerbi_dashboard():
    st.sidebar.markdown("### Power BI Dashboard Setup")

    # Path to the PDF file in the repository
    pdf_file_path = "IFSSA CLEANED DATA.pdf"  # Update this path to the location of your PDF file

    # Check if the PDF file exists
    if os.path.exists(pdf_file_path):
        st.sidebar.markdown("### View Power BI Dashboard PDF")
        st.sidebar.write("Below is the PDF version of the Power BI dashboard.")

        # Display the PDF in the main content area
        st.markdown("### Power BI Dashboard (PDF)")
        st.write("Below is the embedded PDF version of the Power BI dashboard:")

        # Option 1: Use st.pdf_viewer (if available in your Streamlit version)
        try:
            with open(pdf_file_path, "rb") as file:
                st.pdf_viewer(file.read())
        except Exception as e:
            st.warning(f"PDF viewer not available. Error: {e}")
            # Fallback to Option 2: Embed PDF using an iframe
            pdf_embed = f"""
            <iframe
                src="{pdf_file_path}"
                width="100%"
                height="800"
                frameborder="0"
                allowFullScreen="true">
            </iframe>
            """
            components.html(pdf_embed, height=800)
    else:
        st.sidebar.error("The PDF file was not found in the repository.")

def main():
    # Add the header image
    header_image_url = "https://raw.githubusercontent.com/ChiomaUU/Client-Prediction/refs/heads/main/ifssa_2844cc71-4dca-48ae-93c6-43295187e7ca.avif"
    st.image(header_image_url, use_container_width=True)  # Display the image at the top

    st.title("Client Return Prediction App")
    st.write("Enter details to predict if a client will return.")

    # Load the dataset
    data = load_data()

    # Display the dataset (optional)
    if st.checkbox("Show raw data"):
        st.write(data)

   # User input fields (matching the top 5 important features)
    year_month = st.selectbox("Year-Month", ["2024-08", "2024-07", "2024-06"])
    total_visits = st.number_input("Total Visits", min_value=1, max_value=100, step=1)
    avg_days_between_pickups = st.number_input("Avg Days Between Pickups", min_value=1.0, max_value=100.0, step=0.1)
    days_since_last_pickup = st.number_input("Days Since Last Pickup", min_value=0, step=1)

    # Prepare input data
    input_data = {
        "year_month_2024-08": 1 if year_month == "2024-08" else 0,  # One-hot encoding for year-month
        "total_visits": total_visits,
        "avg_days_between_pickups": avg_days_between_pickups,
        "days_since_last_pickup": days_since_last_pickup
    }

    # Prediction button
    if st.button("Predict"):
        if model is None:
            st.error("Model not loaded. Please check if 'model_top5.pkl' exists.")
        else:
            input_df = preprocess_input(input_data)
            prediction = model.predict(input_df)
            probability = model.predict_proba(input_df)
    
            st.subheader("Prediction Result:")
            st.write("✅ Prediction: **Yes**" if prediction[0] == 1 else "❌ Prediction: **No**")
            st.write(f"📊 Probability (Yes): **{probability[0][1]:.4f}**")
            st.write(f"📊 Probability (No): **{probability[0][0]:.4f}**")
    
    # Add Power BI Dashboard to the sidebar
    powerbi_dashboard()

# Run the app
if __name__ == "__main__":
    main()
