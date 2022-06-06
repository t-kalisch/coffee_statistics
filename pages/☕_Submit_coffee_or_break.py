import streamlit as st
from common_functions import *
import datetime
from datetime import date

st.subheader("**:coffee:** Submit a coffee break")
if st.session_state.admin != "1":
  st.warning("You do not have the permissions to submit a coffee or break. Please contact a system administrator for further information.")

elif st.session_state.admin == "1":
  
  st.markdown("Please enter the names and number of coffees for the break.")
  col1,col2,col3,col4,col5,col6,col7,col8 = st.columns([1,1,1,1,1,1,1,1])
  p1_name = col6.text_input("Person 1")
  p2_name = col7.text_input("Person 2")
  p3_name = col8.text_input("Person 3")
  col1,col2,col3,col4,col5,col6,col7,col8 = st.columns([1,1,1,1,1,1,1,1])
  tk = col1.text_input("TK")
  pb = col2.text_input("PB")
  db = col3.text_input("DB")
  flg = col4.text_input("FLG")
  shk = col5.text_input("SHK")
  p1_coffees = col6.text_input("Coffees 1")
  p2_coffees = col7.text_input("Coffees 2")
  p3_coffees = col8.text_input("Coffees 3")
  col1,col2,col3,col4,col5,col6,col7,col8 = st.columns([1,1,1,1,1,1,1,1])
  date_day = col1.text_input("Day", placeholder = datetime.date.today().day)
  date_month = col2.text_input("Month", placeholder = datetime.date.today().month)
  date_year = col3.text_input("Year", placeholder = datetime.date.today().year)
  persons=['TK','PB','DB','FLG','SHK',p1_name,p2_name,p3_name]
  coffees=[tk,pb,db,flg,shk,p1_coffees,p2_coffees,p3_coffees]
  date_br=[date_day,date_month,date_year]
  col1,col2 = st.columns([2,6])
  col1.button("Submit break", on_click=submit_break, args=(persons,coffees,date_br))
  st.write("-" * 34)
  st.write("Enter an extended ID and Name to add a coffee to a break.")
  last_breaks=get_last_breaks(10)
  col1, col2, col3 = st.columns([1,1,3])
  id_ext = col1.text_input("Extended ID", placeholder=last_breaks[len(last_breaks)-1][0])
  coffee_name = col2.text_input("Username", placeholder="User")
  col1.button("Add coffee", on_click=add_coffee_to_break_check, args=(id_ext, coffee_name, logged_in_user))
  df=pd.DataFrame(last_breaks,columns=['Extended ID','Date','Drinkers','Coffees'])
  col3.markdown("Last 10 breaks")
  col3.dataframe(df, width=600, height=500)
