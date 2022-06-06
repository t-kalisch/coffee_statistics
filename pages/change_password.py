import streamlit as st

st.subheader("**:adult:** Change username")
if st.session_state.admin != "1":
    st.markdown("Please enter your current username, password and new username.")
    col1,col2,col3 = st.columns([0.5,1,0.7])
    curr_user = col2.text_input("Username", placeholder = "Username")
    user_pw = col2.text_input("Password", type="password", placeholder = "Password")
    col2.write("-" * 34)
    new_user = col2.text_input("Choose a new username", placeholder = "Username")
    user_change = col2.button("Save new username")
if st.session_state.admin == "1":
    st.markdown("Change username for a member.")
    col1,col2,col3 = st.columns([0.5,1,0.7])
    curr_user = col2.text_input("Old username", placeholder = " Old username")
    user_pw = col2.text_input("New username", placeholder = "New username")
    col2.write("-" * 34)
    new_user = col2.text_input("Please enter your password", type = 'password', placeholder = "Password")
    user_change = col2.button("Confirm")

col2.write("=" * 34)
st.subheader("**:closed_lock_with_key:** Change password")
if st.session_state.admin != "1":
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
    st.markdown("Change password for another person")
    col1,col2,col3 = st.columns([0.5,1,0.7])
    col2.text_input("Username", placeholder = "User")
    col2.text_input("New password", type = 'password', placeholder = "Password")
    col2.write("-" * 34)
    col2.text_input("Please enter your password to confirm", type = 'password', placeholder = "Password")
    col2.button("Confirm")
