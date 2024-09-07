import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import LabelEncoder


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

st.title("Bulk Records - Customer Status and Churn Category Prediction")

# Add a file uploader for CSV files
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the uploaded CSV as a DataFrame
    st.write("Uploaded CSV Data:")
    st.dataframe(df)

    if st.button("Predict"):
        # filling 0.0 GB for customers with no internet service
        df.loc[df['Internet Service'] == 'No', 'Avg Monthly GB Download'] = df.loc[
            df['Internet Service'] == 'No', 'Avg Monthly GB Download'].fillna(0.0)
        # filling 0.0 Charges for customers with no phone services
        df.loc[df['Phone Service'] == 'No', 'Avg Monthly Long Distance Charges'] = df.loc[
            df['Phone Service'] == 'No', 'Avg Monthly Long Distance Charges'].fillna(0.0)
        # customers without internet service cannot have these services
        net_dependent_features = ['Internet Type', 'Online Security', 'Online Backup', 'Device Protection Plan',
                                  'Premium Tech Support', 'Streaming TV', 'Streaming Movies', 'Streaming Music',
                                  'Unlimited Data']
        df.loc[df['Internet Service'] == 'No', net_dependent_features] = df.loc[
            df['Internet Service'] == 'No', net_dependent_features].fillna('No internet service')
        # customers with no phone service cannot opt for multiple lines
        df.loc[df['Phone Service'] == 'No', 'Multiple Lines'] = df.loc[
            df['Phone Service'] == 'No', 'Multiple Lines'].fillna('No phone service')
        # assuming that some customers did not avail any offer
        df['Offer'] = df['Offer'].fillna('No Offer')

        # Encode the categorical variables
        label_encoders = {}
        for col in ['Gender', 'Married', 'City', 'Offer', 'Phone Service', 'Multiple Lines',
                    'Internet Service', 'Internet Type', 'Online Security', 'Online Backup',
                    'Device Protection Plan', 'Premium Tech Support', 'Streaming TV', 'Streaming Movies',
                    'Streaming Music', 'Unlimited Data', 'Contract', 'Paperless Billing', 'Payment Method']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

        # Load models and scaler
        status_model = joblib.load('01VotingRandomStatus.pkl')
        category_model = joblib.load('01VotingRandomCategory.pkl')
        scaler = joblib.load('01VotingRandomScalerStatus.pkl')

        # Ensure the input DataFrame contains only the required features
        X_input = df[['Gender', 'Age', 'Married', 'Number of Dependents', 'City', 'Zip Code',
                      'Latitude', 'Longitude', 'Number of Referrals', 'Tenure in Months',
                      'Offer', 'Phone Service', 'Avg Monthly Long Distance Charges',
                      'Multiple Lines', 'Internet Service', 'Internet Type',
                      'Avg Monthly GB Download', 'Online Security', 'Online Backup',
                      'Device Protection Plan', 'Premium Tech Support', 'Streaming TV',
                      'Streaming Movies', 'Streaming Music', 'Unlimited Data', 'Contract',
                      'Paperless Billing', 'Payment Method', 'Monthly Charge',
                      'Total Charges', 'Total Refunds', 'Total Extra Data Charges',
                      'Total Long Distance Charges', 'Total Revenue']]

        # Scale the input data
        X_input_scaled = scaler.transform(X_input)

        # Predict Customer Status
        df['Predicted Customer Status'] = status_model.predict(X_input_scaled)

        # Calculate churn probabilities
        churn_probabilities = status_model.predict_proba(X_input_scaled)[:, 1]  # Probability of churn


        # Determine Risk Group
        def get_risk_group(probability):
            scaled_prob = probability * 10
            if 5 <= scaled_prob < 6:
                return "Low Risk"
            elif 6 <= scaled_prob < 7.5:
                return "Medium Risk"
            elif scaled_prob >= 7.5:
                return "High Risk"
            else:
                return "Not in Risk Range"


        df['Churn Probability'] = churn_probabilities
        df['Predicted Risk Group'] = df['Churn Probability'].apply(get_risk_group)

        # Predict Churn Category for those predicted as churned
        df['Predicted Churn Category'] = df.apply(
            lambda row: category_model.predict([X_input_scaled[df.index.get_loc(row.name)]])[0]
            if row['Predicted Customer Status'] == 1 else 'Not Churned', axis=1)

        # Decode the predictions according to the provided mappings
        status_mapping = {1: 'Churned', 0: 'Stayed'}
        category_mapping = {
            0: 'Attitude',
            1: 'Competitor',
            2: 'Dissatisfaction',
            5: 'No Churn Category',
            4: 'Other',
            3: 'Price'
        }

        df['Predicted Customer Status'] = df['Predicted Customer Status'].map(status_mapping)
        df['Predicted Churn Category'] = df['Predicted Churn Category'].replace('Not Churned', 5).map(category_mapping)

        # Show the output per each record
        st.write("Predicted Output Data:")
        st.dataframe(df[['Predicted Customer Status', 'Predicted Churn Category', 'Predicted Risk Group']])

        # Save the output to a new CSV
        output_df = df.copy()
        output_file_path = '/Users/udani/Desktop/MSC/pycharm projects/WebApp/test_with_predictions.csv'
        output_df.to_csv(output_file_path, index=False)

        # Display download link for the CSV
        st.markdown(f"### Download Predicted CSV File:")
        with open(output_file_path, "rb") as file:
            btn = st.download_button(
                label="Download CSV",
                data=file,
                file_name="predicted_output.csv",
                mime="text/csv"
            )

        # Count the number of 'Stayed' and 'Churned' customers
        status_counts = df['Predicted Customer Status'].value_counts()

        # Plot the bar chart for customer status
        st.write("### Customer Status Counts")
        fig, ax = plt.subplots()
        bars = status_counts.plot(kind='bar', ax=ax, color=['green', 'red'])
        ax.set_xlabel("Customer Status")
        ax.set_ylabel("Count")
        ax.set_title("Counts of Stayed and Churned Customers")
        # Add counts on top of bars
        for bar in bars.containers:
            ax.bar_label(bar, fmt='%d', label_type='edge', padding=3)
        st.pyplot(fig)

        # Count the number of each churn category
        churn_category_counts = df['Predicted Churn Category'].value_counts()

        # Plot the bar chart for churn category
        st.write("### Churn Category Counts")
        fig, ax = plt.subplots()
        bars = churn_category_counts.plot(kind='bar', ax=ax, color='blue')
        ax.set_xlabel("Churn Category")
        ax.set_ylabel("Count")
        ax.set_title("Counts of Each Churn Category")
        # Add counts on top of bars
        for bar in bars.containers:
            ax.bar_label(bar, fmt='%d', label_type='edge', padding=3)
        st.pyplot(fig)

        # Count the number of each risk group
        risk_group_counts = df['Predicted Risk Group'].value_counts()

        # Plot the bar chart for risk groups
        st.write("### Risk Group Counts")
        fig, ax = plt.subplots()
        bars = risk_group_counts.plot(kind='bar', ax=ax, color=['yellow', 'orange', 'red'])
        ax.set_xlabel("Risk Group")
        ax.set_ylabel("Count")
        ax.set_title("Counts of Each Risk Group")
        # Add counts on top of bars
        for bar in bars.containers:
            ax.bar_label(bar, fmt='%d', label_type='edge', padding=3)
        st.pyplot(fig)
