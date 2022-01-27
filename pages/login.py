import streamlit as st
import numpy as np
import pandas as pd
from pages import utils

# @st.cache
def app():
    st.markdown("## Login")
    st.write("Please log in with your username and password")
    
    user = st.text_input(label="", placeholder="Username")
    user_pw = st.text_input(label="", type="password")#, placeholder="Password")
    login = st.checkbox("Login", help="You will be logged in while the checkbox is ticked")
