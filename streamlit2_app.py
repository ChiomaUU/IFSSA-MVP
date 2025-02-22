import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# Simulate loading a dataset (for demonstration purposes)
@st.cache_data
def load_data():
    # Create a dummy dataset with equal-length columns
    data = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],  # 5 rows
        'household': [0, 1, 0, 1, 0],  # 5 rows (0 = No, 1 = Yes)
        'time_since_previous_visit': [1, 2, 3, 4, 5],  # 5 rows
        'contact_frequency': ['weekly', 'monthly', 'weekly', 'monthly', 'weekly'],  # 5 rows
        'returned': [1, 0, 1, 0, 1]  # Target column (1 = returned, 0 = did not return)
    })
    return data

# Simulate a prediction (rule-based)
def predict(input_data):
    # Example rule: If age > 30 and household == 1, predict "likely to return"
    if input_data['age'].values[0] > 30 and input_data['household'].values[0] == 1:
        return [1]  # Likely to return
    else:
        return [0]  # Unlikely to return

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
    st.title("Power BI Dashboard PDF Viewer")
    st.write("This app demonstrates how to display a PDF version of a Power BI dashboard in Streamlit.")

    # Call the Power BI dashboard function
    powerbi_dashboard()

if __name__ == "__main__":
    main()
# Main function to run the app
def main():
    # Add the header image
    header_image_url = "https://raw.githubusercontent.com/ChiomaUU/Client-Prediction/refs/heads/main/ifssa_2844cc71-4dca-48ae-93c6-43295187e7ca.avif"
    st.image(header_image_url, use_container_width=True)  # Display the image at the top

    st.title("Client Return Prediction App (MVP)")
    st.write("This app predicts whether a client will return for food hampers.")

    # Load the dataset
    data = load_data()

    # Display the dataset (optional)
    if st.checkbox("Show raw data"):
        st.write(data)

    # Input fields for user to enter data
    st.header("Input Features")
    input_features = {}

    # Create input fields for each feature
    input_features['age'] = st.number_input("Enter Age", min_value=0, max_value=100, value=30)
    input_features['household'] = st.selectbox("Is the client part of a household?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    input_features['time_since_previous_visit'] = st.number_input("Enter Time Since Previous Visit (in months)", min_value=0, value=1)
    input_features['contact_frequency'] = st.selectbox("Contact Frequency", options=["weekly", "monthly"])

    # Convert input to DataFrame
    input_df = pd.DataFrame([input_features])

    # Make prediction
    if st.button("Predict"):
        prediction = predict(input_df)
        st.subheader("Prediction Result")
        if prediction[0] == 1:
            st.success("The client is likely to return.")
        else:
            st.error("The client is unlikely to return.")

    # Add Power BI Dashboard to the sidebar
    powerbi_dashboard()

# Run the app
if __name__ == "__main__":
    main()
