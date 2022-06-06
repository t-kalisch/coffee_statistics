import streamlit as st
st.set_page_config(page_title="Coffee list",page_icon="chart_with_upwards_trend",layout="wide")
from collections import namedtuple
import math
import pandas as pd
import numpy as npy
import datetime
from datetime import date
import plotly
import plotly.express as px
import mysql.connector as mysql
import extra_streamlit_components as stx
import plotly.graph_objects as go
from data_collection import *
#from calculations import *

@st.cache(allow_output_mutation=True, suppress_st_warning = True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

user_data=get_user_data()
simple_data=get_simple_data()
all_func=get_functionals()


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


#@st.cache(suppress_st_warning=True)
def check_login(user, user_pw):                         #login check
    if user == "guest":
        g_pw = get_guest_pw()
        if user_pw == g_pw:
            login_check = True
            admin_status = 2
    else:
        login_check=False
        user_data=get_user_data()
        for i in range(len(user_data)):
            if user == user_data[i][0] and user_pw == user_data[i][1]:
                login_check = True
                admin_status=user_data[i][2]
    if login_check == True:
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
        st.session_state.attempt="true"
        st.session_state.logged_in = "false"
        st.session_state.user_name = ""
        st.session_state.admin = "0"
        #cookie_manager.set("logged_in", False, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_false")
        #cookie_manager.delete("user")
        logged_in = "false"


#@st.cache(suppress_st_warning=True)       
def logout_check():
    cookie_manager.set("logged_in", "false", expires_at=datetime.datetime(year=2030, month=1, day=1), key="logout")
    cookie_manager.set("status", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="del_admin_status")
    cookie_manager.set("user", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user")
    st.session_state.attempt="false"
    st.session_state.logged_in = "false"
    st.session_state.user_name = None
    st.session_state.admin = "0"
    logged_in = "false"
 

def add_coffee_to_break_check(id_ext, coffee_name, logged_in_user):
    if id_ext=="":
        id_ext = last_breaks[len(last_breaks)-1][0]
    add_coffee_to_break(id_ext, coffee_name, logged_in_user)

def delete_one_coffee_check(del_id,del_person):
    if del_id=="":
        del_id = last_breaks[len(last_breaks)-1][0]
    delete_one_coffee(del_id,del_person)
  


with st.sidebar:
    
    col1,col2 = st.columns([1,1.65])
    user = col1.text_input(label="", placeholder="Username", key="user")
    user_pw = col2.text_input(label="", type="password", placeholder="Password", key="user_pw")
    col1,col2=st.columns([1,1.65])
    if logged_in == "true":
        logout = col1.button("Logout", help="Log out here", on_click=logout_check)
    else:
        login = col1.button("Login", help="Log in here", on_click=check_login, args=(user, user_pw))
    remember = st.checkbox("Remember me", help="Keep me logged in (uses cookies)")      
      
if logged_in == "true":
    st.title("Logged in as {}".format(logged_in_user))
    if admin_status == "1":
        col2.write("  Status: Administrator")
    elif admin_status == "2":
        col2.write("  Status: guest")
    else:
        col2.write("  Member status: User") 
        
    #if logout:
    #    logout_check()
else:
    st.title("Welcome to the future of coffee drinking **:coffee:**")
    st.write("In order to get access to the visualised data you need to be logged in with your username and password.")
