import streamlit as st
from common_functions import *
import pandas as pd
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")


    #---------------------- deleting a break by knowing id_ext ----------------
def clear_one_break(del_id, test):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    
    if del_id == "":
         st.warning("Please enter a break ID")
    else:
        cursor.execute("SELECT * FROM breaks WHERE id_ext='"+del_id+"'")
        del_break=cursor.fetchall()

        if del_break != []:
            cursor.execute("DELETE FROM breaks WHERE id_ext='"+del_id+"'")
            cursor.execute("update update_status set last_break = timestamp(subdate(current_date, 1))")
            st.success("Break "+del_id+" has successfully been deleted.")
        else:
           st.error("Break "+del_id+" does not exist, therefore nothing was deleted.")
		
    db.commit()
    db.close()

    
#----------------------- check whether break ID was entered or not --------------------------
def delete_one_coffee_check(del_id,del_person):
    if del_id=="":
        del_id = last_breaks[len(last_breaks)-1][0]
    delete_one_coffee(del_id,del_person)
    
    
	 #---------------------- deleting a coffee from a break ----------------
def delete_one_coffee(id_ext, name):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	
	cursor.execute("select persons, coffees from drinkers where id_ext = '"+id_ext+"'")
	tmp=cursor.fetchall()
	persons = tmp[0][0].split("-")
	coffees = tmp[0][1].split("-")

	for i in range(len(persons)):
		if persons[i] == name.upper():
			coffees[i] = int(coffees[i]) - 1
			cursor.execute("update mbr_"+name.upper()+" set n_coffees = "+str(coffees[i])+" where id_ext = '"+id_ext+"'")
		if coffees[i] == 0:
			cursor.execute("delete from mbr_"+name.upper()+" where id_ext = '"+id_ext+"'")

	persons_new = ""
	coffees_new = ""
	for i in range(len(persons)):
		if coffees[i] == 0:
			pass
		else:
			if persons_new == "":
				persons_new += persons[i]
				coffees_new += str(coffees[i])
			else:
				persons_new = persons_new + "-" + persons[i]
				coffees_new = coffees_new + "-" + str(coffees[i])
	if persons_new == "":
		cursor.execute("DELETE FROM breaks WHERE id_ext='"+id_ext+"'")
	else:
		cursor.execute("update drinkers set persons = '"+persons_new+"' where id_ext = '"+id_ext+"'")
		cursor.execute("update drinkers set coffees = '"+coffees_new+"' where id_ext = '"+id_ext+"'")
	db.commit()
	db.close()



    
    
    
    
    

########################################################################################################################################################################
#####################################################    MAIN    #######################################################################################################
########################################################################################################################################################################
st.subheader("**:x:** Delete a coffee break")
if 'logged_in' not in st.session_state or 'user_name' not in st.session_state or 'admin' not in st.session_state or 'attempt' not in st.session_state:
    st.warning("Warning! Your session was terminated due to inactivity. Please return to home to restart it and regain access to all features.")
else:

	
	if st.session_state.admin != "1":
	  st.warning("You do not have the permission to delete a coffee or break. Please contact a system administrator for further information.")

	elif st.session_state.admin == "1":
	  st.markdown("Please enter the extended ID of the break you want to delete.")
	  last_breaks=get_last_breaks(10)
	  col1,col2,col3 = st.columns([1,0.5,3])
	  del_id = col1.text_input("Extended ID of break", placeholder=last_breaks[len(last_breaks)-1][0])
	  df=pd.DataFrame(last_breaks,columns=['Extended ID','Date','Drinkers','Coffees'])
	  col3.markdown("Last 10 breaks")
	  col3.dataframe(df, width=600, height=400)
	  delete = col1.button("Delete break", on_click=clear_one_break, args=(del_id,""))
	  col1.write("-" * 34)
	  del_person = col1.text_input("Delete for person", placeholder="Username")
	  col1.button("Delete coffee from break", on_click=delete_one_coffee_check, args=(del_id,del_person))


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
