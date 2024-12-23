import streamlit as st
from generate_quiz import generate_quiz
from generate_assignment import generate_assignment
from generate_paper import generate_paper
from generate_ppt import generate_ppt
from tutor import tutor
from styles import overall_css

# Set up app configuration and title
st.set_page_config(page_title="Virtual Course Instructor", layout="wide")
st.markdown(overall_css, unsafe_allow_html=True)
# Create a grid layout with four columns for the buttons
col1, col2, col3, col4, col5 = st.columns(5)

# Display buttons to select page in a row at the top of each page
with col1:
    quiz_button = st.button("**Quiz**")

with col2:
    assignment_button = st.button("**Assignment**")

with col3:
    paper_button = st.button("**Paper**")

with col4:
    ppt_button = st.button("**Slide**")

with col5:
    tutor_button = st.button("**tutor**")

# Get current page from session state
current_page = st.session_state.get("page", "generate_quiz")

# Update session state based on button clicks
if quiz_button:
    current_page = "generate_quiz"
elif assignment_button:
    current_page = "generate_assignment"
elif paper_button:
    current_page = "generate_paper"
elif ppt_button:
    current_page = "generate_ppt"
elif tutor_button:
    current_page = "tutor"

# Save the current page to session state
st.session_state.page = current_page

# Page content
if current_page == "generate_quiz":
    generate_quiz()

elif current_page == "generate_assignment":
    generate_assignment()

elif current_page == "generate_paper":
    generate_paper()

elif current_page == "generate_ppt":
    generate_ppt()

elif current_page == "tutor":
    tutor()






# def set_background_image(image_path):
#     """
#     Set a background image for the Streamlit app.
#     :param image_path: str, path to the background image
#     """
#     # Read the image file
#     with open(image_path, "rb") as image_file:
#         image_bytes = image_file.read()
    
#     # Encode the image in base64
#     import base64
#     encoded_image = base64.b64encode(image_bytes).decode()
    
#     # Define the CSS to set the background image
#     background_image_style = f"""
#     <style>
#     .stApp {{
#         background: url(data:image/jpg;base64,{encoded_image});
#         background-size: cover;
#     }}
#     </style>
#     """
    
#     # Add the CSS to the Streamlit app
#     st.markdown(background_image_style, unsafe_allow_html=True)

# # Path to the background image
# image_path = "./Resources/2.png"

# # Call the function to set the background image
# set_background_image(image_path)