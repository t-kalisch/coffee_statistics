import streamlit as st
import numpy as np
import pandas as pd
from pages import utils

# @st.cache
st.subheader("**:calendar:** Enter holidays")
if admin_status == "1":
    col1, col2, col3, col4 = st.columns([0.5,1,1,1])
    month = col1.text_input("Month", placeholder=datetime.date.today().month)
    year = col2.text_input("Year", placeholder=datetime.date.today().year)
    person_hol = col3.text_input("Person", placeholder = "User")
    holidays = col4.text_input("Number of holidays", placeholder=0)
    if person_hol == "":
        sub_hol = st.button("Submit holidays", help="Submit holidays for yourself", on_click=submit_holidays, args=(st.session_state.user_name, month, year, holidays))
        #if sub_hol:
        #    submit_holidays(st.session_state.user_name, month, year, holidays)
    else:
        sub_hol = st.button("Submit holidays", help="Submit holidays for "+person_hol, on_click=submit_holidays, args=(person_hol,month,year,holidays))
        #if sub_hol:
        #    submit_holidays(person_hol, month, year, holidays)

    st.write("-" * 34)   
    st.subheader("All holidays")
    all_holidays = get_all_holidays(datetime.datetime.now())
    #print(all_holidays)
    names=get_members()
    columns=["ID","Tot. work days"]
    for i in range(len(names)):
        columns.append(names[i])
    #st.write(all_holidays)
    df=pd.DataFrame(all_holidays,columns=columns)
    st.dataframe(df, width=1000, height=1000)

else:
    col1, col2, col3 = st.columns([0.5,1,2])
    month = col1.text_input("Month", placeholder=datetime.date.today().month)
    year = col2.text_input("Year", placeholder=datetime.date.today().year)
    holidays = col3.text_input("Number of holidays", placeholder=0)
    sub_hol = col1.button("Submit", help="Submit holidays")
    if sub_hol:
        submit_holidays(st.session_state.user_name, month, year, holidays)
    st.write("-" * 34)   
    st.subheader("All holidays")
    all_holidays = get_all_holidays(datetime.datetime.now())
    #print(all_holidays)
    holidays_person=[]
    names=get_members()
    columns=["Month","Total work days"]
    for i in range(len(names)):
        if names[i] == st.session_state.user_name:
            columns.append(names[i])
            for j in range(len(all_holidays)):
                temp=[]
                temp.append(all_holidays[j][0])
                temp.append(all_holidays[j][i+2])
                temp.append(all_holidays[j][1])
                holidays_person.append(temp)
    df=pd.DataFrame(holidays_person,columns=columns)
    st.dataframe(df, width=1000, height=1000)
