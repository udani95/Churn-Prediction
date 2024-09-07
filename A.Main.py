import streamlit as st
import base64


def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string

# Load your local image (replace 'background_image.png' with your file name)
img_file = "blue-corner-gradient-free-png.png"
base64_image = get_base64_image(img_file)

img_file2 = "img01.png"  # Replace with your image file for the center
base64_image2 = get_base64_image(img_file2)


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


st.title("Telco Churn Analysis and Prediction")


center_img_html = f"""
<div style="text-align: center; padding: 5px;">
    <img src="data:image/png;base64,{base64_image2}" style="max-width: 100%; max-height: 1000px;" />
</div>
"""

st.markdown(center_img_html, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    Welcome to the Telco Churn Analysis and Prediction web application.<br>
    This tool is designed to help you understand and predict customer churn based on various features such as demographics, service usage, and customer interactions.<br>
    Explore the different pages to visualize churn statistics, predict churn status, and analyze customer behavior to optimize retention strategies.
</div>
""", unsafe_allow_html=True)