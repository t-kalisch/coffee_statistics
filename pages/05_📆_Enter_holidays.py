import streamlit as st
import numpy as np
import pandas as pd
#from pages import utils
import datetime
from datetime import date
import math
import re
from common_functions import *
import mysql.connector as mysql
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")



#----------------------- holiday input ----------------------------------------
def submit_holidays(name, month_inp, year_inp, days_inp):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("create table if not exists holidays (id int auto_increment, month int, work_days int, primary key(id))")            #creating holidays table
    
    if int(month_inp) > 12 or int(year_inp) < 2020:
        st.error("Invalid date: The date you entered does not exist or lies before the age of the coffee list!")
    else:
        if int(month_inp) < 10:
            month_id = int(year_inp+"0"+month_inp)
        else:
            month_id = int(year_inp+month_inp)
    
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='coffee_list' AND TABLE_NAME='holidays' AND column_name='"+name.upper()+"'")     #check if name already exists
        tmp = cursor.fetchall()
        if tmp[0][0] == 0:
            cursor.execute("alter table holidays add "+name.upper()+" int")     #adding name if doesn't exist yet

        month_id_all = get_months(datetime.date(2020,11,1))[1]
        for i in range(len(month_id_all)):
            cursor.execute("select count(*) from holidays where month like "+str(month_id_all[i]))
            tmp = cursor.fetchall()
            if tmp[0][0] == 0:
                cursor.execute("insert into holidays (month, work_days) values (%s, %s)", (month_id_all[i], work_days[i]))

        cursor.execute("select "+name.upper()+" from holidays where month = "+str(month_id))
        tmp=cursor.fetchall()
        if tmp[0][0] == None:
            cursor.execute("update holidays set "+name.upper()+" = "+str(int(days_inp))+" where month like "+str(month_id))
        else:
            cursor.execute("update holidays set "+name.upper()+" = "+str(int(days_inp)+tmp[0][0])+" where month like "+str(month_id))
        st.success("The holidays have successfully been saved.")

    db.commit()
    db.close()


#--------------------------- getting all holidays ------------------------------
#@st.cache
def get_all_holidays(timestamp):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select * from holidays")
	tmp=cursor.fetchall()
	
	holidays=[]
	for i in range(len(tmp)):
		temp=[]
		for j in range(len(tmp[i])-1):
			if tmp[i][j+1] == None:
				temp.append(0)
			else:
				temp.append(int(tmp[i][j+1]))
		holidays.append(temp)
	db.close()
	return holidays

    
########################################################################################################################################################################
#####################################################    MAIN    #######################################################################################################
########################################################################################################################################################################
st.subheader("**:calendar:** Enter holidays")
if 'logged_in' not in st.session_state or 'user_name' not in st.session_state or 'admin' not in st.session_state or 'attempt' not in st.session_state:
    st.warning("Warning! Your session was terminated due to inactivity. Please return to home to restart it and regain access to all features.")
else:

    if st.session_state.admin == "1":
        col1, col2, col3, col4 = st.columns([0.5,1,1,1])
        month = col1.text_input("Month", placeholder=datetime.date.today().month)
        year = col2.text_input("Year", placeholder=datetime.date.today().year)
        person_hol = col3.text_input("Person", placeholder = "User")
        holidays = col4.text_input("Number of holidays", placeholder=0)
        if person_hol == "":
            if month == "" and year == "":
                #sub_hol = st.button("Submit holidays", help="Submit holidays for yourself", on_click=submit_holidays, args=(st.session_state.user_name, datetime.date.today().month, datetime.date.today().year, holidays))
                sub_hol = st.button("Submit holidays")	#inactive button
            else:
                #sub_hol = st.button("Submit holidays", help="Submit holidays for yourself", on_click=submit_holidays, args=(st.session_state.user_name, month, year, holidays))
                sub_hol = st.button("Submit holidays")	#inactive button
        else:
            if month == "" and year == "":
                #sub_hol = st.button("Submit holidays", help="Submit holidays for "+person_hol, on_click=submit_holidays, args=(person_hol,datetime.date.today().month,datetime.date.today().year,holidays))
                sub_hol = st.button("Submit holidays")	#inactive button
            else:
                #sub_hol = st.button("Submit holidays", help="Submit holidays for "+person_hol, on_click=submit_holidays, args=(person_hol,month,year,holidays))
                sub_hol = st.button("Submit holidays")	#inactive button

        st.write("-" * 34)   
        st.subheader("All holidays")
        #all_holidays = get_all_holidays(datetime.datetime.now())
        all_holidays = [[202011,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],			#last values before closing server
			[202012,20,3,6,0,3,6,6,0,0,0,0,0,0,0,0,0,0,0],
			[202101,19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202102,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202103,23,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
			[202104,20,0,4,0,0,2,0,10,0,0,0,0,0,0,0,0,0,0],
			[202105,19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202106,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202107,22,12,1,0,5,4,1,0,0,0,0,0,0,0,0,0,0,0],
			[202108,22,0,10,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0],
			[202109,22,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202110,21,0,2,0,1,5,0,0,0,0,0,0,0,0,0,0,0,0],
			[202111,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202112,21,6,6,0,4,5,6,0,4,0,0,0,0,0,0,0,0,0],
			[202201,21,10,0,0,0,5,11,0,0,0,0,0,0,0,0,0,0,0],
			[202202,19,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
			[202203,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202204,19,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
			[202205,21,7,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
			[202206,20,16,13,0,0,0,3,0,0,0,0,20,0,0,0,0,0,0],
			[202207,21,15,15,0,5,5,5,0,5,0,0,5,0,0,0,0,0,0],
			[202208,23,10,10,0,10,0,0,0,19,0,0,0,0,0,0,0,0,0],
			[202209,22,4,2,0,0,4,0,0,22,0,0,4,0,0,0,0,0,0],
			[202210,20,0,4,0,0,0,0,0,0,0,0,0,0,19,0,0,0,0],
			[202211,21,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202212,19,4,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0],
			[202301,22,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0],
			[202302,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202303,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202304,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202305,20,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202306,21,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202307,21,7,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0],
			[202308,23,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202309,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202310,21,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],
			[202311,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202312,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	    
        #print(all_holidays)
        #names=get_members()
        names = ["TK","PB","NV","DB","FLG","SHK","TB","TT","RS","VB","MR","KKM","SB","SK","AK","GP","DM"]           #last values before closing server
        columns=["ID","Tot. work days"]
        for i in range(len(names)):
            columns.append(names[i])
        #st.write(all_holidays)
        df=pd.DataFrame(all_holidays,columns=columns)
        st.dataframe(df, width=1000, height=1000)

    elif st.session_state.admin == "0":
        col1, col2, col3 = st.columns([0.5,1,2])
        month = col1.text_input("Month", placeholder=datetime.date.today().month)
        year = col2.text_input("Year", placeholder=datetime.date.today().year)
        holidays = col3.text_input("Number of holidays", placeholder=0)
        #sub_hol = col1.button("Submit", help="Submit holidays")
        sub_hol = False
        sub_hol_dumme = col1.button("Submit")	#inactive button
        if sub_hol:
            submit_holidays(st.session_state.user_name, month, year, holidays)
        st.write("-" * 34)   
        st.subheader("All holidays")
        #all_holidays = get_all_holidays(datetime.datetime.now())
        all_holidays = [[202011,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],			#last values before closing server
			[202012,20,3,6,0,3,6,6,0,0,0,0,0,0,0,0,0,0,0],
			[202101,19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202102,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202103,23,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
			[202104,20,0,4,0,0,2,0,10,0,0,0,0,0,0,0,0,0,0],
			[202105,19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202106,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202107,22,12,1,0,5,4,1,0,0,0,0,0,0,0,0,0,0,0],
			[202108,22,0,10,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0],
			[202109,22,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202110,21,0,2,0,1,5,0,0,0,0,0,0,0,0,0,0,0,0],
			[202111,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202112,21,6,6,0,4,5,6,0,4,0,0,0,0,0,0,0,0,0],
			[202201,21,10,0,0,0,5,11,0,0,0,0,0,0,0,0,0,0,0],
			[202202,19,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
			[202203,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202204,19,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
			[202205,21,7,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
			[202206,20,16,13,0,0,0,3,0,0,0,0,20,0,0,0,0,0,0],
			[202207,21,15,15,0,5,5,5,0,5,0,0,5,0,0,0,0,0,0],
			[202208,23,10,10,0,10,0,0,0,19,0,0,0,0,0,0,0,0,0],
			[202209,22,4,2,0,0,4,0,0,22,0,0,4,0,0,0,0,0,0],
			[202210,20,0,4,0,0,0,0,0,0,0,0,0,0,19,0,0,0,0],
			[202211,21,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202212,19,4,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0],
			[202301,22,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0],
			[202302,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202303,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202304,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202305,20,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202306,21,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202307,21,7,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0],
			[202308,23,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202309,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202310,21,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],
			[202311,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[202312,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        #print(all_holidays)
        holidays_person=[]
        #names=get_members()
        names = ["TK","PB","NV","DB","FLG","SHK","TB","TT","RS","VB","MR","KKM","SB","SK","AK","GP","DM"]           #last values before closing server
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

    else:
        st.warning("You do not have the permissions to submit holidays. Please contact a system administrator for further information.")
    

	#------- footer ----------------
footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color:  grey;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by P. C. Brehm and T. Kalisch. Web design by T. Kalisch <a style='display: block; text-align: center</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
