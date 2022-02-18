import os
import streamlit as st
import numpy as np
import datetime
import extra_streamlit_components as stx
from PIL import  Image

# Custom imports 
from app import MultiPage
from pages import login, change_password, test2 # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
#display = Image.open('Logo.png')
#display = np.array(display)
# st.image(display, width = 400)

st.title("Data Storyteller Application")
logged_in=False
# Add all your application here
app.add_page("Login", login.app)
app.add_page("Change password", change_password.app)
app.add_page("Test2", test2.app)


# The main app
app.run()
