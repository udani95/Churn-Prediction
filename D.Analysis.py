import streamlit as st
import base64
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

centered_title = """
<style>
.centered-title {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px; /* Adjust this value if you want to add more or less space after the title */
}
</style>
"""

st.markdown(centered_title, unsafe_allow_html=True)

# Center and style the title
st.markdown('<div class="centered-title"><h1>Analysis of Existing Records</h1></div>', unsafe_allow_html=True)


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

# Load the sidebar image
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

# Load the existing CSV file
file_path = "/Users/udani/Desktop/MSC/MSCResearch/New/telecom_customer_churn.csv"
df = pd.read_csv(file_path)

# Counting "Stayed" and "Churned" Customers in the Customer Status column
status_counts = df['Customer Status'].value_counts()

# Counting Churn Categories
churn_category_counts = df['Churn Category'].value_counts()

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

with col1:
    st.subheader('Customer Status Count')
    st.bar_chart(status_counts, use_container_width=True)

with col2:
    st.subheader('Churn Category Count')
    st.bar_chart(churn_category_counts, use_container_width=True)

# Center and style the subheader
st.markdown('<div class="centered-subheader"><h2>Churn Count Variation in Map</h2></div>', unsafe_allow_html=True)

# Show the number of churn records identified on the map
churned_df = df[df['Customer Status'] == 'Churned']
m = folium.Map(location=[churned_df['Latitude'].mean(), churned_df['Longitude'].mean()], zoom_start=10)
marker_cluster = MarkerCluster().add_to(m)

for idx, row in churned_df.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=f"Churn Category: {row['Churn Category']}\nCity: {row['City']}").add_to(marker_cluster)

# Display the map in Streamlit with centered alignment
st_folium(m, width=700, height=500)

# Calculate and display the top 20 cities with the highest churn counts
city_churn_counts = churned_df['City'].value_counts()
top_20_city_churn_counts = city_churn_counts.head(20)

# CSS to center the subheader and add space after it
centered_subheader = """
<style>
.centered-subheader {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px; /* Adjust the value to add more or less space */
}
</style>
"""

st.markdown(centered_subheader, unsafe_allow_html=True)

# Center and style the subheader
st.markdown('<div class="centered-subheader"><h2>Top 20 Cities with Most Churned Customers</h2></div>', unsafe_allow_html=True)

# Define the number of columns for displaying the top 20 cities
num_columns = 2
cols = st.columns(num_columns)  # Create columns for grid layout

# CSS to center text within each column
centered_text = """
<style>
.centered-text {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}
</style>
"""
st.markdown(centered_text, unsafe_allow_html=True)

# Display the top 20 cities and their churn counts in a grid format
for i, (city, count) in enumerate(top_20_city_churn_counts.items()):
    with cols[i % num_columns]:
        st.markdown(f'<div class="centered-text"><strong>{city}</strong>: {count} churned customers</div>', unsafe_allow_html=True)


# Pie charts and counts for users with specified features
features = [
    'Internet Service',
    'Online Security',
    'Online Backup',
    'Device Protection Plan',
    'Premium Tech Support',
    'Streaming TV',
    'Streaming Movies',
    'Streaming Music',
    'Unlimited Data',
    'Contract',
    'Payment Method'
]

#Center and style the subheader
st.markdown('<div class="centered-subheader"><h2>Proportions of Users with Specific Features</h2></div>', unsafe_allow_html=True)


# Create a dataframe to store churn counts per feature
feature_churn_counts = {}

# Define the number of columns for pie charts
num_columns = 3
cols = st.columns(num_columns)  # Create 3 columns for pie charts

# Set figure size for consistent pie charts
figsize = (4, 4)

# Calculate and display pie charts with titles and churn counts
for i, feature in enumerate(features):
    # Calculate churn counts for feature values
    feature_churn_counts[feature] = churned_df[feature].value_counts()

    # Create the pie chart
    feature_counts = df[feature].value_counts()
    labels = feature_counts.index
    sizes = feature_counts.values

    fig, ax = plt.subplots(figsize=figsize)  # Consistent size for pie charts
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#66b35f'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(feature, fontsize=14)  # Add title to each pie chart

    with cols[i % num_columns]:
        st.pyplot(fig)


#Center and style the subheader
st.markdown('<div class="centered-subheader"><h2>Churn Counts for Each Feature</h2></div>', unsafe_allow_html=True)


# Define the number of columns for displaying churn counts
cols = st.columns(num_columns)  # Reuse the same number of columns

for i, (feature, counts) in enumerate(feature_churn_counts.items()):
    with cols[i % num_columns]:
        st.write(f"**{feature}**")
        st.write(counts)
