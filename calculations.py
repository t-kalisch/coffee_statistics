import streamlit as st
import math
import mysql.connector as mysql
import numpy
import datetime
from datetime import date
import pandas as pd
from plotly import *
import plotly.express as px
from common_functions import *



#----------------------------------------- getting monthly coffees from database --------------------------------------
#@st.cache(allow_output_mutation=True)
def get_monthly_coffees(names, month_id):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select * from monthly_coffees")
	tmp=cursor.fetchall()
	
	monthly_coffees_all=[]
	monthly_coffees=[]
	total_monthly_coffees=[]
	for i in range(len(month_id)):
		total=0
		temp=[]
		for j in range(len(names)):
			temp.append(tmp[j][i+2])
			total += tmp[j][i+2]
		monthly_coffees.append(temp)
		total_monthly_coffees.append(total)
		
	monthly_coffees_all.append(monthly_coffees)
	monthly_coffees_all.append(total_monthly_coffees)
	db.close()
	return monthly_coffees_all





#-------------------------- getting total coffees from database
def get_total_coffees(names):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    coffees=[]
    for i in range(len(names)):
        cursor.execute("select coffees from total_coffees where name like '"+names[i]+"'")
        coffees.append(cursor.fetchall()[0][0])
    db.close()
    return coffees


#--------------------------- calculating monthly ratios from database -----------------------------
def get_monthly_ratio(names, month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True) 
    monthly_ratio=[]
    monthly_coffees = get_monthly_coffees(names, month_id)
    
    for i in range(len(month_id)):
        temp=[]
        for j in range(len(names)):
            if monthly_coffees[1][i] == 0:
                ratio=0
            else:
                ratio=100*monthly_coffees[0][i][j]/monthly_coffees[1][i]
            temp.append(ratio)
        monthly_ratio.append(temp)
    db.close()
    return monthly_ratio



#------------------ getting expectation values from database, maybe recalculating if functional has been updated ------
def get_expectation_values(names, month_id, func_selected):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("select active_func from update_status")
    tmp=cursor.fetchall()

    if tmp[0][0] != func_selected:
        update="full"

        write_exp_values_dev(names, month_id, func_selected, update)
        cursor.execute("update update_status set active_func = '"+func_selected+"'")
        db.commit()

        
    cursor.execute("select * from exp_values where month = "+max(month_id))
    tmp=cursor.fetchall()

    exp_values=[]
    for i in range(len(tmp[0])-2):
        exp_values.append(float(tmp[0][i+2]))
    db.close()
    return exp_values

#----------------------- getting standard deviations from database, does not recalculate if functional has been updated! ---
def get_stdev(names, month_id):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select * from exp_values_stdev where month = "+str(month_id[len(month_id)-1]))
	tmp=cursor.fetchall()
    
	stdev=[]
	for i in range(len(names)):
		stdev.append(float(tmp[0][i+2]))
	db.close()
	return stdev

#------------------------- getting the MAD for every functional ---------------------------------------------------
def get_mad(names, month_id):
    db = init_connection()
    cursor=db.cursor(buffered=True)

    param = get_parameters()
    cursor.execute("select name, MAD from func_param")
    tmp = cursor.fetchall()

    mad_total=[]
    for i in range(len(tmp)):
        temp=[]
        temp.append(tmp[i][0])
        temp.append(float(tmp[i][1]))
        mad_total.append(temp)
    db.close()
    return mad_total

#----------------------------- getting the coffee prize history -----------------------------------------
def get_prizes(names, month_id, func_selected):
    db = init_connection()
    cursor=db.cursor(buffered=True)


    cursor.execute("select active_func from update_status")
    tmp=cursor.fetchall()

    if tmp[0][0] != func_selected:
        update="full"
        write_exp_values_dev(names, month_id, func_selected, update)
        write_prizes(names, month_id)
        cursor.execute("update update_status set active_func = '"+func_selected+"'")
        db.commit()

    cursor.execute("select * from prize_history")
    tmp=cursor.fetchall()
    
    prizes_sizes=[["Kaffeemeister", "Hotshot", "Genosse"],[40,25,10]]
    total_data=[]        
    for i in range(len(month_id)-1):
        for j in range(3):
            temp = []
            temp.append(str(tmp[i][1]))
            for k in range(len(names)):
                if names[k] == tmp[i][2+j]:
                    temp.append(k)
            temp.append(prizes_sizes[0][j])
            temp.append(prizes_sizes[1][j])
            total_data.append(temp)
 
    db.close()
    return total_data


#----------------------------- getting all weekly breaks and weekly coffees ------------------------------
def get_weekly_coffees_breaks(names):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    weekly_data=[]

    cursor.execute("select week_id, breaks, coffees from weekly_data")
    tmp = cursor.fetchall()

    for i in range(len(tmp)):
        temp=[]
        temp.append(tmp[i][0])
        temp.append(tmp[i][1])
        temp.append(tmp[i][2])
        weekly_data.append(temp)
    db.close()
    return weekly_data

#--------------------------- getting correlations between drinkers ------------------------------------
def get_correlation(names):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    corr_all=[]
    tot_coffees = get_total_coffees(names)

    corr_abs=[]
    corr_rel=[]
    for i in range(len(names)):

        cursor.execute("select "+names[i]+" from corr_abs")             #getting absolute correlation from table corr_abs
        temp_abs=cursor.fetchall()

        cursor.execute("select "+names[i]+" from corr_rel")             #getting relative correlation from table corr_rel
        temp_rel=cursor.fetchall()

        temp1=[]
        temp2=[]
        for j in range(len(names)):
            temp1.append(temp_abs[j][0])
            temp2.append(float(temp_rel[j][0]))
        corr_abs.append(temp1)                              #writing into array
        corr_rel.append(temp2)
    corr_all.append(corr_abs)
    corr_all.append(corr_rel)
    db.close()
    return corr_all


#----------------------------- getting time resolved correlation data ----------------------------------------
def get_corr_time(names, month_id_start, month_id_end):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='212.227.72.95',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    n_months=0
    all_corr_raw=[]
    abs_corr_data=[]
    rel_corr_data=[]
    for i in range(len(names)):
        cursor.execute("select * from corr_"+names[i]+" where month >= "+month_id_start+" and month <= "+month_id_end)
        tmp = cursor.fetchall()
        abs_corr_data_person = []
        rel_corr_data_person = []
        
        for j in range(len(names)):
            n_corr = 0
            n_corr_rel = 0
            n_tot_coffees = 0
            for k in range(len(tmp)):
                n_corr += tmp[k][j+2]
                n_tot_coffees += tmp[k][1]
            rel_corr_data_person.append(round(100*n_corr/n_tot_coffees,1))
            abs_corr_data_person.append(n_corr)
        abs_corr_data.append(abs_corr_data_person)
        rel_corr_data.append(rel_corr_data_person)
		

        all_corr_raw.append(tmp)
    db.close()
	        
	
	
    return rel_corr_data                    #returns all data in 3D array of tuples: all_corr_data[names][month][name_to_correlate]



#----------------------------- getting the percentage of total breaks per month and in total per person ------------------------
def get_perc_breaks(names, month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    percentage=[]
    total_percentage=[]
    cursor.execute("select * from percentage_breaks")
    tmp = cursor.fetchall()

    for i in range(len(tmp)):
        temp=[]
        for j in range(len(names)):
            temp.append(float(tmp[i][j+2]))
        percentage.append(temp)
    db.close()
    return percentage

#---------------------------- calculating total breaks per month ---------------------------------------------
def get_tot_br_p_m(month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    total_breaks=[]
    for i in range(len(month_id)):
        cursor.execute("select count(id_ext) from breaks where id_ext like '"+str(month_id[i])+"%'")
        tmp = cursor.fetchall()

        for j in range(len(tmp)):
            total_breaks.append(tmp[j][0])
    db.close()
    return total_breaks

#---------------------------- calculating monthly and total coffees per work day ------------------------
def get_coffees_per_work_day(names, month_id):  
    db = init_connection()
    cursor = db.cursor(buffered=True)
    coffees_per_work_day = []
    
    workdays = get_work_days(names, month_id)           #getting monthly work days
    total_workdays=[]
    total_p_w=[]

    for i in range(len(names)):
        total_workdays.append(0)                        #creating total workdays array
    
    cursor.execute("select * from monthly_coffees")     #getting monthly coffees
    tmp = cursor.fetchall()
    temp1=[]

    for i in range(len(month_id)):
        temp=[]
        for j in range(len(names)):
            if workdays[i][j] == 0:
                temp.append(0)
            else:
                temp.append(round(tmp[j][i+2]/workdays[i][j],3))     #dividing monthly coffees by monthly work days
            total_workdays[j]=total_workdays[j]+workdays[i][j] 	 #getting total workdays per person
        temp1.append(temp)
    
    cursor.execute("select coffees from total_coffees")
    tmp=cursor.fetchall()
    for i in range(len(names)):
        total_p_w.append(round(tmp[i][0]/total_workdays[i],3))
        
    coffees_per_work_day.append(total_p_w)
    coffees_per_work_day.append(temp1)
    db.close()
    return coffees_per_work_day


#----------------------------- calculating break sizes per month per person and total --------------------
def get_break_sizes_per_month(names, month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True)
    break_sizes=[]
    break_sizes_total=[]
    for i in range(len(month_id)):
        #break_sizes.append(round(total/len(tmp),2))
        temp=[]

        for j in range(len(names)):
            cursor.execute("select size from break_sizes inner join mbr_"+names[j]+" on break_sizes.id_ext = mbr_"+names[j]+".id_ext where mbr_"+names[j]+".id_ext like '"+str(month_id[i])+"%'")
            tmp=cursor.fetchall()
            #print(tmp)
            total=0
            for k in range(len(tmp)):
                total = total + tmp[k][0]
            if len(tmp) == 0:
                temp.append(0)
            else:
                temp.append(round(total/len(tmp),2))
                
        cursor.execute("select size from break_sizes where id_ext like '"+str(month_id[i])+"%'")
        tmp=cursor.fetchall()
        #print(tmp)
        total=0
        for j in range(len(tmp)):
            total = total + tmp[j][0]
        break_sizes_total.append(round(total/len(tmp),2))
        
        break_sizes.append(temp)
    break_sizes.append(break_sizes_total)
    db.close()
    return break_sizes


#-------------------------------------- calculating social scores -------------------------------------------------
def get_social_score(names, month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True)

    social_score_total=[]

    cursor.execute("select * from social_score")
    tmp=cursor.fetchall()
    social_score_total.append(list(tmp[0]))
    social_score_total[0].pop(0)
    social_score_total[0].pop(0)
    for i in range(len(social_score_total[0])):
        social_score_total[0][i] = float(social_score_total[0][i])
    
    temp=[]
    for i in range(len(tmp)-1):
        temp.append(list(tmp[i+1]))
        temp[i].pop(0)
        temp[i].pop(0)
        for j in range(len(temp[i])):
            temp[i][j] = float(temp[i][j])
    social_score_total.append(temp)
    #print(social_score_total)

    db.close()
    return social_score_total



#----- calculating all holiday corrections, namely recalculating factor for work days of month and damping factor -----
def holiday_corrections(names, month_id):   
    db = init_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("select * from holidays where month > 202102")       #getting holidays
    tmp = cursor.fetchall()
    
    correction_factors=[]
    total=[]
    holidays=[]
    for i in range(len(month_id)):
        total.append(tmp[i][2])
        temp1=[]
        for j in range(len(names)):
            if tmp[i][j+3] == None:
                temp1.append(1)
            else:
                f_damp = (1-((tmp[i][j+3]/tmp[i][2])**2))               #damping function: f = 1 - (d_hol/t_tot)^2
                p_wd = (total[i]-tmp[i][j+3])/total[i]                  #correction for holidays: d_tot-d_hol / d_tot
                temp1.append(f_damp/p_wd)                               #scaling month according to holidays: 1/p_wd; multiplying with damping factor
        correction_factors.append(temp1)
    return correction_factors

#-------------------------- calculating the cumulated coffees from database -------------------------------
def get_cumulated_coffees(names, month_id):
    all_coffees=get_monthly_coffees(names, month_id)[0]         #getting monthly coffees

    coffees_cumulated=[]

    for i in range(len(month_id)):
        coffees=[]
        if i > 0:
            for j in range(len(names)):
                    coffees.append(coffees_cumulated[i-1][j]+all_coffees[i][j])  #adding up monthly coffees
        else:
            for j in range(len(names)):
                  coffees.append(all_coffees[i][j])
        coffees_cumulated.append(coffees)
    
    return coffees_cumulated


#------------------------- getting work days per month per person ------------------------
#@st.cache
def get_work_days(names, month_id):
    db = init_connection()
    cursor = db.cursor(buffered=True)
	
    cursor.execute("select * from holidays")            #getting holidays
    tmp = cursor.fetchall()

    workdays=[]
    for i in range(len(month_id)):
        temp=[]
        for j in range(len(names)):
            if tmp[i][j+3] == None:
                temp.append(tmp[i][2])
            else:
                temp.append(tmp[i][2]-tmp[i][j+3])
        workdays.append(temp)
    db.close()
    return workdays

#------------------------- getting all functional parameters -------------------
def get_parameters():
    db = init_connection()
    cursor = db.cursor(buffered=True)

    cursor.execute("select * from func_param")
    tmp = cursor.fetchall()

    parameters=[]
    for i in range(len(tmp)):
        temp=[]
        for j in range(8):
            temp.append(tmp[i][j+1])
        parameters.append(temp)
    db.close()
    return parameters

#-------------------------- calculating standard deviation of deviations etc ---------------------------------
def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

#------------------------- getting the MAD for given functional ---------------------------------------------------
def calc_mad_corr(names, month_id, func):
    func_data = calc_exp_values_dev(names, month_id, func)

    ratio =  0.2

    total_mad=0
    total_stdev=0
    counter=0
    for i in range(len(func_data[1])):
        for j in range(len(names)):
             counter += 1
             total_mad += abs(func_data[1][i][j])
    mad = total_mad/counter
    counter=0
    for i in range(len(func_data[2])):
        for j in range(len(names)):
            if func_data[2][i-1][j] != 0 and func_data[2][i][j] != 0:
                counter += 1
                total_stdev += func_data[2][i][j]
    m_stdev = total_stdev/counter

    mad_corr = ratio * mad + (1-ratio) * m_stdev
    
    return round(mad_corr,2)

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
