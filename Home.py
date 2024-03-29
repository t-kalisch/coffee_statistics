import streamlit as st
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")
from collections import namedtuple
import math
import pandas as pd
import numpy as npy
import datetime
from datetime import date
import plotly
import plotly.express as px
import mysql.connector as mysql
import plotly.graph_objects as go
import extra_streamlit_components as stx
from common_functions import *
from calculations import update_database
from PIL import Image

@st.cache(allow_output_mutation=True, suppress_st_warning = True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

#user_data=get_user_data()
user_data = [["TK","akstr!admin2",1],            #values before closing server
		 ["PB","akstr!admin",1],
		 ["NV","niklasv123",0],
		 ["DB","ClW8YSxD",0],
		 ["FLG","baddragon",0],
		 ["SHK","cumcocoon",0],
		 ["TB","czLwp2BP",0],
		 ["TT","19SZs4lL",0],
		 ["RS","N5SgG5N+",0],
		 ["VB","s*3wq5fI",0],
		 ["MR","g1iUKkVk",0],
		 ["KKM","j4h6cYVC",0],
		 ["SB","3GTo6yGk",0],
		 ["SK","GttoY3Jk",0],
		 ["AK","xErIbJA8",0],
		 ["GP","xy8m9bef5f5xm",0],
		 ["DM","pimmel",0]]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in=cookie_manager.get(cookie="logged_in")
if 'user_name' not in st.session_state:
    st.session_state.user_name=cookie_manager.get(cookie="user")
if 'admin' not in st.session_state:
    st.session_state.admin=cookie_manager.get(cookie="status")
if 'attempt' not in st.session_state:
    st.session_state.attempt="false"
    
    
if cookie_manager.get(cookie="logged_in") == "true":
    st.session_state.logged_in="true"
    st.session_state.user_name = cookie_manager.get(cookie="user")
    st.session_state.admin=cookie_manager.get(cookie="status")

logged_in=st.session_state.logged_in
logged_in_user=st.session_state.user_name
admin_status=st.session_state.admin


#---------------------------- login function
#@st.cache(suppress_st_warning=True)
def check_login(user, user_pw):                         #login check
    if user == "guest":
        #g_pw = get_guest_pw()
        g_pw = "Fn+P4za8"
        if user_pw == g_pw:
            login_check = True
            admin_status = 2
    else:
        login_check=False
        #user_data=get_user_data()
        for i in range(len(user_data)):
            if user == user_data[i][0] and user_pw == user_data[i][1]:
                login_check = True
                admin_status=user_data[i][2]
    if login_check == True:
        st.success("You have successfully logged into the coffee list!")
        st.session_state.logged_in = "true"
        st.session_state.user_name = user
        st.session_state.admin = str(admin_status)
        st.session_state.attempt = "false"
        if remember:
            cookie_manager.set("logged_in", True, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_true")
            cookie_manager.set("user", user, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user")
            cookie_manager.set("status", admin_status, expires_at=datetime.datetime(year=2030, month=1, day=1), key="admin_status")
        else:
            cookie_manager.set("logged_in", False, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logout")
            cookie_manager.set("status", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="del_admin_status")
            cookie_manager.set("user", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user")            
    else:
        st.warning("Incorrect username/password.")
        st.session_state.attempt="true"
        st.session_state.logged_in = "false"
        st.session_state.user_name = ""
        st.session_state.admin = "0"
        #cookie_manager.set("logged_in", False, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_false")
        #cookie_manager.delete("user")
        logged_in = "false"
 
#---------------------------- logout function
#@st.cache(suppress_st_warning=True)       
def logout_check():
    cookie_manager.set("logged_in", "false", expires_at=datetime.datetime(year=2030, month=1, day=1), key="logout")
    cookie_manager.set("status", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="del_admin_status")
    cookie_manager.set("user", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user")
    st.session_state.attempt="false"
    st.session_state.logged_in = "false"
    st.session_state.user_name = None
    st.session_state.admin = None
    logged_in = "false"
        

########################################################################################################################################################################
#####################################################    MAIN    #######################################################################################################
########################################################################################################################################################################        



if st.session_state.logged_in == "true":
    st.title("Logged in as {}".format(st.session_state.user_name))
    col1, col2 = st.columns([1,2.5])
    col1.write("You now have access to the coffee list.")
    if st.session_state.admin == "1":
        col2.write("  Status: Administrator")
    elif st.session_state.admin == "2":
        col2.write("  Status: guest")
    elif st.session_state.admin == "0":
        col2.write("  Member status: User") 
    logout = st.button("Logout", help="Log out here", on_click=logout_check)
    with st.sidebar:
          if st.session_state.admin == "1":
              update = st.button("Update", help="Update database", on_click=update_database)

else:
    st.title("Welcome to the future of coffee drinking **:coffee:**")
    st.write("In order to get access to the visualised data you need to be logged in with your username and password.")

    col1,col2,col3 = st.columns([1,1,2])
    user = col1.text_input(label="", placeholder="Username", key="user")
    user_pw = col2.text_input(label="", type="password", placeholder="Password", key="user_pw")
    login = col1.button("Login", help="Log in here", on_click=check_login, args=(user, user_pw))
    remember = col2.checkbox("Remember me", help="Keep me logged in (uses cookies)")              

image = Image.open('cheers.jpg')
st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    
#------- footer ----------------
footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color:  grey;
text-align: right;
}
</style>
<div class="footer">
<p>Developed by P. C. Brehm and T. Kalisch. Web design by T. Kalisch <a style='display: block; text-align: center</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
