import streamlit as st
import numpy as np
import pandas as pd
from pages import utils

# @st.cache
def app():
    st.markdown("## Login")
    st.write("Please log in with your username and password")
    
    
    user_data=[['TK', 'akstr!admin2',1],['PB','akstr!admin2',1],['NV',None,None],['DB',None,None],['FLG','baddragon',None],['SHK',None,None],['TB',None,None],['TT',None,None],['RS',None,None]]
    logged_in=False
    admin_status=0

    
    
    user = st.text_input(label="", placeholder="Username")
    user_pw = st.text_input(label="", type="password")#, placeholder="Password")
    login = st.checkbox("Login", help="You will be logged in while the checkbox is ticked")

    if login:
        for i in range(len(user_data)):
            if user == user_data[i][0] and user_pw == user_data[i][1]:
                admin_status=user_data[i][2]
                logged_in=True
    if logged_in==True:
        st.write("Successfully logged in!")
    return logged_in
