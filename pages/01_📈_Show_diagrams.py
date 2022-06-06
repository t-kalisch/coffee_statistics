import streamlit as st
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")
from common_functions import *



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
