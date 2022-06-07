import streamlit as st
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")
from common_functions import *
import datetime
from datetime import date


  #------------------------ getting functionals from database ------------------
def get_functionals():
    db = init_connection()
    cursor = db.cursor(buffered=True)

    cursor.execute("select name from func_param")
    tmp=cursor.fetchall()

    func_names=[]
    for i in range(len(tmp)):
        func_names.append(tmp[i][0])
    db.close()
    return sorted(func_names, key=str.lower)

#------------------------- getting active functional from database -------------------
def get_active_func():
    db = init_connection()
    cursor = db.cursor(buffered=True)

    cursor.execute("select active_func from update_status")
    func = cursor.fetchall()
    db.close()
    return func[0][0]



########################################################################################################################################################################
#####################################################    MAIN    #######################################################################################################
########################################################################################################################################################################
st.subheader("**:chart_with_upwards_trend:** Visualised data")
simple_data=get_simple_data()

col1,col2,col3,col4 = st.columns([1,1,1,1])
col1.subheader(str(simple_data[0][0])+" drinkers")
col1.subheader(str(simple_data[1][0])+" active drinkers")
col2.subheader(str(simple_data[2][0])+" months of drinking")
col3.subheader(str(simple_data[3][0])+" coffee breaks")
col3.subheader(str(simple_data[4][0])+" cups of coffee")
col4.subheader(str(simple_data[5][0])+" data sets")
col4.subheader(str(simple_data[6][0])+" diagrams")
st.write("-" * 34)

if st.session_state.logged_in != "true":
  st.warning("You need to be logged in to get access to the visualised data.")

  all_func = get_functionals()
  
with st.sidebar:
    act_func = get_active_func()
    if st.session_state.logged_in == "true":
        if st.session_state.admin == "1":
            for i in range(len(all_func)):
                if all_func[i] == act_func:
                    curr=i
            func_selected = st.selectbox("Functional selector", all_func, curr)
        else:
            act_func_l=[]
            act_func_l.append(act_func)
            func_selected = st.selectbox("Active functional", act_func_l, 0)

    st.title("Available diagrams:")
    coffees_monthly = st.checkbox("Monthly coffees")
    coffees_total = st.checkbox("Total coffees / Monthly ratios")
    expectation_data = st.checkbox("Expectation values / Prize history")
    c_b_weekly = st.checkbox ("Weekly breaks and coffees")
    correlation = st.checkbox("Correlation")
    break_percentage = st.checkbox("Percentages of breaks")
    soc_sc = st.checkbox("Social score")
    coffees_pwd = st.checkbox("Coffees per work day")
    coffees_cumulated = st.checkbox("Cumulated coffees")  
  
  
