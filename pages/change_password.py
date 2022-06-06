import streamlit as st
from common_functions import *

if st.session_state.admin != "1":
    st.subheader("**:adult:** Change username")
    st.markdown("Please enter your current username, password and new username.")
    col1,col2,col3 = st.columns([0.5,1,0.7])
    curr_user = col2.text_input("Username", placeholder = "Username")
    user_pw = col2.text_input("Password", type="password", placeholder = "Password")
    col2.write("-" * 34)
    new_user = col2.text_input("Choose a new username", placeholder = "Username")
    user_change = col2.button("Save new username")

    st.write("-" * 34)
    st.subheader("**:closed_lock_with_key:** Change password")
    st.markdown("You can change your password here.")
    col1,col2,col3 = st.columns([0.5,1,0.7])
    curr_pw = col2.text_input("Current password", type="password", placeholder = "Old password")
    col2.write("-" * 34)
    col1,col2,col3 = st.columns([0.5,1,0.7])
    pw_new = col2.text_input("Choose a new password", type="password", placeholder = "New password")
    conf_pw = col2.text_input("Repeat the new password", type="password", placeholder = "Repeat password")
    pw_change = col2.button("Save new password")
    if pw_new != conf_pw:
        st.error("The entered new passwords differ from each other")
    if pw_change:
        if pw_new == "" or conf_pw == "":
            st.error("You cannot enter an empty password")
        else:
            done=False
            for i in range(len(user_data)):
                if st.session_state.user_name == user_data[i][0] and curr_pw == user_data[i][1]:
                    done = change_profile_data(st.session_state.user_name, "", pw_new, st.session_state.admin)
            if done == False:
                st.warning("Incorrect password")

if st.session_state.admin == "1":
    st.subheader("**:closed_lock_with_key:** Change the profile of a member")
    st.markdown("You can enter a new username and password for a member, or change their member status.")
    st.markdown("Guest password: "+get_guest_pw())
    col1,col2,col3 = st.columns([0.5,1,0.7])
    change_user = col1.text_input("User", placeholder = "Username")
    username_new = col2.text_input("New username", placeholder = "Username")
    pw_new = col2.text_input("New password", type = "password", placeholder = "Password")
    status=-1
    if change_user != "":
        for i in range(len(user_data)):
            if user_data[i][0] == change_user:
                if user_data[i][2] == 1:
                    status=1
                    status_str="Admin"
                else:
                    status=0
                    status_str="User"
    col1,col2 = st.columns([0.5,1.7])
    if status == -1:
        col1.selectbox ("Change member status", (""), 0)
    else: 
        user_status = col1.selectbox ("Change member status", ("User", "Admin"), status)
    st.write("-" * 34)
    col1,col2 = st.columns([0.5,0.5])
    admin_pw = col1.text_input("Please enter your password to confirm", type = 'password', placeholder = "Password")
    confirm = col1.button("Confirm")
    if confirm:
        if status == -1:
            st.error("Wrong username entered")
        else:
            done=False
            for i in range(len(user_data)):
                if st.session_state.user_name == user_data[i][0] and admin_pw == user_data[i][1]:
                    done = change_profile_data(change_user, username_new, pw_new, user_status)
            if done == False:
                st.warning("Incorrect password")
