import streamlit as st
import mysql.connector as mysql

#---------------------------------------- initiates connection to database -----------------------------------------
#@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return mysql.connect(**st.secrets["mysql"])

#----------------------------------------- getting all members from database ---------------------------------------
#@st.cache
def get_members():
    db = init_connection()
    cursor = db.cursor(buffered=True)

    names=[]

    cursor.execute("select name from members")              #getting all members tables
    mbrs=cursor.fetchall()
    mbrs=list(mbrs)
    for i in range(len(mbrs)):
        names.append(mbrs[i][0])
    db.close()
    return names

#------------------------------------ getting guest password from database ------------------------------------
def get_guest_pw():
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select guest_pw from update_status")
	pw=cursor.fetchall()[0][0]
	db.close()
	return pw

#------------------------------------ getting all user data ------------------------------------------
def get_user_data():
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select name, password, admin from members")
	user_data=cursor.fetchall()
	db.close()
	return user_data

#----------------------------------- getting simple data ------------------------------------------
def get_simple_data():							# getting simple data from database
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select value from simple_data")
	simple_data=cursor.fetchall()

	db.close()
	return simple_data

#----------------------------- getting last 10 breaks from database ---------------------------------
#@st.cache
def get_last_breaks(last_break):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select * from breaks order by id_ext desc limit "+str(last_break))
	breaks=cursor.fetchall()
	cursor.execute("select * from drinkers order by id_ext desc limit "+str(last_break))
	drinkers=cursor.fetchall()

	last_breaks=[]
	for i in range(len(breaks)):
		temp=[]
		date=str(breaks[len(breaks)-i-1][2])+"."+str(breaks[len(breaks)-i-1][3])+"."+str(breaks[len(breaks)-i-1][4])
		temp.append(breaks[len(breaks)-i-1][1])
		temp.append(date)
		temp.append(drinkers[len(drinkers)-i-1][2])
		temp.append(drinkers[len(drinkers)-i-1][3])
		last_breaks.append(temp)
	db.close()
	return last_breaks

