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
