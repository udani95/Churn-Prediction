import streamlit as st
import base64
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np


# Function to load image and convert to base64 string
def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string


# Load your local image (replace 'background_image.png' with your file name)
img_file = "blue-corner-gradient-free-png.png"
base64_image = get_base64_image(img_file)

# Set the background using local image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{base64_image}");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

img_file1 = "images (1).jpeg"
base64_image1 = get_base64_image(img_file1)

# Set the background for the sidebar using local image
sidebar_bg_img = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{base64_image1}");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
}}
</style>
"""

st.markdown(sidebar_bg_img, unsafe_allow_html=True)

st.title("Single Record - Customer Status and Churn Category Prediction")

# Input fields with dropdown selections
input_data = {}

# Dropdowns for categorical fields
input_data['Gender'] = st.selectbox("Gender", ['Female', 'Male'])
input_data['Age'] = st.number_input("Age", min_value=0, max_value=100)
input_data['Married'] = st.selectbox("Married", ['Yes', 'No'])
input_data['Number of Dependents'] = st.number_input("Number of Dependents", min_value=0, max_value=10)
input_data['City'] = st.text_input("City")
input_data['Zip Code'] = st.number_input("Zip Code")
input_data['Latitude'] = st.number_input("Latitude", format="%.6f")
input_data['Longitude'] = st.number_input("Longitude", format="%.6f")
input_data['Number of Referrals'] = st.number_input("Number of Referrals", min_value=0, max_value=100)
input_data['Tenure in Months'] = st.number_input("Tenure in Months", min_value=0, max_value=120)
input_data['Offer'] = st.selectbox("Offer", ['No Offer', 'Offer E', 'Offer D', 'Offer A', 'Offer B', 'Offer C'])
input_data['Phone Service'] = st.selectbox("Phone Service", ['Yes', 'No'])
input_data['Avg Monthly Long Distance Charges'] = st.number_input("Avg Monthly Long Distance Charges", format="%.2f")
input_data['Multiple Lines'] = st.selectbox("Multiple Lines", ['No', 'Yes', 'No phone service'])
input_data['Internet Service'] = st.selectbox("Internet Service", ['Yes', 'No'])
input_data['Internet Type'] = st.selectbox("Internet Type", ['Cable', 'Fiber Optic', 'DSL', 'No internet service'])
input_data['Avg Monthly GB Download'] = st.number_input("Avg Monthly GB Download", min_value=0, max_value=1000)
input_data['Online Security'] = st.selectbox("Online Security", ['No', 'Yes', 'No internet service'])
input_data['Online Backup'] = st.selectbox("Online Backup", ['Yes', 'No', 'No internet service'])
input_data['Device Protection Plan'] = st.selectbox("Device Protection Plan", ['No', 'Yes', 'No internet service'])
input_data['Premium Tech Support'] = st.selectbox("Premium Tech Support", ['Yes', 'No', 'No internet service'])
input_data['Streaming TV'] = st.selectbox("Streaming TV", ['Yes', 'No', 'No internet service'])
input_data['Streaming Movies'] = st.selectbox("Streaming Movies", ['No', 'Yes', 'No internet service'])
input_data['Streaming Music'] = st.selectbox("Streaming Music", ['No', 'Yes', 'No internet service'])
input_data['Unlimited Data'] = st.selectbox("Unlimited Data", ['Yes', 'No', 'No internet service'])
input_data['Contract'] = st.selectbox("Contract", ['One Year', 'Month-to-Month', 'Two Year'])
input_data['Paperless Billing'] = st.selectbox("Paperless Billing", ['Yes', 'No'])
input_data['Payment Method'] = st.selectbox("Payment Method", ['Credit Card', 'Bank Withdrawal', 'Mailed Check'])
input_data['Monthly Charge'] = st.number_input("Monthly Charge", format="%.2f")
input_data['Total Charges'] = st.number_input("Total Charges", format="%.2f")
input_data['Total Refunds'] = st.number_input("Total Refunds", format="%.2f")
input_data['Total Extra Data Charges'] = st.number_input("Total Extra Data Charges", format="%.2f")
input_data['Total Long Distance Charges'] = st.number_input("Total Long Distance Charges", format="%.2f")
input_data['Total Revenue'] = st.number_input("Total Revenue", format="%.2f")

# Convert the input data to a DataFrame
input_df = pd.DataFrame([input_data])

# Display the DataFrame (optional, for debugging)
st.write("Input Data as DataFrame:")
st.write(input_df)

# Encode other categorical variables
label_encoders = {}
for col in ['Gender', 'Married', 'City', 'Offer', 'Phone Service', 'Multiple Lines',
            'Internet Service', 'Internet Type', 'Online Security', 'Online Backup',
            'Device Protection Plan', 'Premium Tech Support', 'Streaming TV', 'Streaming Movies',
            'Streaming Music', 'Unlimited Data', 'Contract', 'Paperless Billing', 'Payment Method']:
    le = LabelEncoder()
    input_df[col] = le.fit_transform(input_df[col])
    label_encoders[col] = le

# Load the trained models and scaler
status_model = joblib.load('01VotingRandomStatus.pkl')
category_model = joblib.load('01VotingRandomCategory.pkl')
scaler = joblib.load('01VotingRandomScalerStatus.pkl')

# Define the mapping from labels to churn category names
churn_category_mapping = {
    0: 'Attitude',
    1: 'Competitor',
    2: 'Dissatisfaction',
    3: 'Price',
    4: 'Other',
    5: 'No Churn Category'
}

# Ensure the input DataFrame contains only the required features
X_input = input_df[['Gender', 'Age', 'Married', 'Number of Dependents', 'City', 'Zip Code',
                    'Latitude', 'Longitude', 'Number of Referrals', 'Tenure in Months',
                    'Offer', 'Phone Service', 'Avg Monthly Long Distance Charges',
                    'Multiple Lines', 'Internet Service', 'Internet Type',
                    'Avg Monthly GB Download', 'Online Security', 'Online Backup',
                    'Device Protection Plan', 'Premium Tech Support', 'Streaming TV',
                    'Streaming Movies', 'Streaming Music', 'Unlimited Data', 'Contract',
                    'Paperless Billing', 'Payment Method', 'Monthly Charge',
                    'Total Charges', 'Total Refunds', 'Total Extra Data Charges',
                    'Total Long Distance Charges', 'Total Revenue']]

# Scale the features
X_scaled = scaler.transform(X_input)

# Add custom CSS to style and center-align elements
st.markdown("""
    <style>
    .centered {
        text-align: center;
        margin-top: 10px;
    }
    .stButton > button {
        background-color: white;
        color: black;
        border-radius: 8px;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Use HTML to center-align elements
st.markdown('<div class="centered">', unsafe_allow_html=True)
if st.button("Predict"):
    # Predict customer status
    y_status_pred = status_model.predict(X_scaled)
    y_status_prob = status_model.predict_proba(X_scaled)[:, 1]  # Probability of churn

    # Determine the churn probability scaled to 0-10
    churn_probability = y_status_prob[0] * 10

    # Determine the risk group based on churn probability
    if 5 <= churn_probability < 6:
        risk_group = "Low Risk"
    elif 6 <= churn_probability < 7.5:
        risk_group = "Medium Risk"
    elif churn_probability >= 7.5:
        risk_group = "High Risk"
    else:
        risk_group = "Not in Risk Range"

    # Predict churn category and add suggestions
    if y_status_pred[0] == 1:  # If customer is predicted to churn
        churn_category_label = category_model.predict(X_scaled)[0]
        churn_category = churn_category_mapping[churn_category_label]

        # Define recommendations based on churn category
        recommendations = {
            'Competitor': [
                "Reward long-term customers with discounts, upgrades, bonus offers.",
                "Offer flexible contracts with options for early upgrades or downgrades without heavy penalties.",
                "Provide some personalized offers."
            ],
            'Dissatisfaction': [
                "Contact individually and get feedback.",
                "Ensure high network reliability and coverage. Implement rapid resolution processes for service outages or issues.",
                "Enhance customer support by providing 24/7 availability, multi-channel support (phone, chat, email), and reducing wait times.",
                "Develop a dedicated team to handle escalations and resolve issues quickly to prevent dissatisfaction from escalating into churn."
            ],
            'Attitude': [
                "Do regular check-ins, personalized communications.",
                "Reach out proactively to address concerns.",
                "Involve customers in decision-making processes or beta testing new products, making them feel valued."
            ],
            'Price': [
                "Offer clear and straightforward pricing structures with no hidden fees to build trust.",
                "Focus on the value offered—bundle services, provide extra features, or offer premium services.",
                "Provide targeted discounts or promotional offers to price-sensitive customers."
            ],
            'Other': [
                "Contact individually and get feedback.",
                "Do regular check-ins, personalized communications."
            ]
        }

        suggestion = recommendations.get(churn_category, ["No specific recommendation available."])
        suggestion = '\n'.join(suggestion)  # Join the list of suggestions into a single string
        churn_category_prob = category_model.predict_proba(X_scaled)[0]  # Get probability for each class
    else:
        churn_category = "Not Churned"
        suggestion = "No suggestion available as customer did not churn."
        churn_category_prob = None  # No churn category since customer did not churn

    # Map the predicted status to "Will Churn" or "Will Stay"
    status_mapping = {1: "Will Churn", 0: "Will Stay"}
    mapped_status_pred = [status_mapping[status] for status in y_status_pred]

    # Add the predictions and suggestions back to the DataFrame
    input_df['Predicted Status'] = mapped_status_pred
    input_df['Predicted Churn Category'] = churn_category
    input_df['Churn Probability (scaled to 0-10)'] = churn_probability
    input_df['Risk Group'] = risk_group
    input_df['Recommendation'] = [suggestion]

    # Include only the relevant columns for the output
    output_df = input_df[
        ['Predicted Status', 'Predicted Churn Category', 'Churn Probability (scaled to 0-10)', 'Risk Group',
         'Recommendation']]

    # Display the prediction result as a table
    st.write("Prediction Result:")
    st.table(output_df)

    # Provide a download link for the prediction result as a CSV file
    csv_output = output_df.to_csv(index=False)
    st.download_button(
        label="Download Prediction Results as CSV",
        data=csv_output,
        file_name="prediction_results.csv",
        mime="text/csv"
    )

st.markdown('</div>', unsafe_allow_html=True)
