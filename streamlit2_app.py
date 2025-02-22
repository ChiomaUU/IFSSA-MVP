import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

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
    # Input for Power BI Embed URL in the sidebar
    powerbi_url = st.sidebar.text_input(
        "Enter Power BI Embed URL:",
        "https://app.powerbi.com/links/TjI-nyea44?ctid=e228c3df-233f-49c3-9d75-1ce285b59c78&pbi_source=linkShare"
    )

    # Check if a valid URL is provided
    if powerbi_url:
        st.sidebar.markdown("### Power BI Dashboard")
        st.sidebar.write("Interact with the embedded Power BI dashboard below:")

        # Display the Power BI dashboard in the main content area
        st.markdown("### Power BI Dashboard")
        st.write("Below is the embedded Power BI dashboard:")

        # Embed the Power BI Report using an iframe
        powerbi_embed = f"""
        <iframe
            title="Power BI Report"
            width="100%"
            height="800"
            src="{powerbi_url}"
            frameborder="0"
            allowFullScreen="true">
        </iframe>
        """
        # Use components.html to render the iframe
        components.html(powerbi_embed, height=800)
    else:
        st.sidebar.warning("Please enter a valid Power BI embed link.")
 
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
