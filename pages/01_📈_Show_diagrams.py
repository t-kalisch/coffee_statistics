import streamlit as st
st.set_page_config(page_title="Coffee list",page_icon="coffee",layout="wide")
from common_functions import *
import datetime
from datetime import date
from calculations import *
import plotly.graph_objects as go

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
st.header("**:chart_with_upwards_trend:** Visualised data")
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

    
else:
    all_func = get_functionals()
    with st.sidebar:
        act_func = get_active_func()
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
        all_diagrams = st.checkbox("Show all")
        coffees_monthly = st.checkbox("Monthly coffees")
        coffees_total = st.checkbox("Total coffees / Monthly ratios")
        expectation_data = st.checkbox("Expectation values / Prize history")
        c_b_weekly = st.checkbox ("Weekly breaks and coffees")
        correlation = st.checkbox("Correlation")
        break_percentage = st.checkbox("Percentages of breaks")
        soc_sc = st.checkbox("Social score")
        coffees_pwd = st.checkbox("Coffees per work day")
        coffees_cumulated = st.checkbox("Cumulated coffees")  

        
    names = get_members()
    month_info=get_months(datetime.date(2021,3,8))
    months_dly=month_info[0]
    month_id_dly=month_info[1]
    month_info=get_months(datetime.date(2020,11,1))
    months_all=month_info[0]
    month_id_all=month_info[1]
    
    #-------------------------------------------------------------------------------------------------------------- monthly coffees, per person + total (line + bar chart)
    if coffees_monthly or all_diagrams:
        st.subheader("Coffees per month") 
        
        monthly_coffees_all = get_monthly_coffees(names, month_id_all)
        df = pd.DataFrame(monthly_coffees_all[0], columns=names, index=months_all)    #coffees per month per person

        fig1 = px.line(df, title="Number of coffees per month per person", labels={"variable":"", "index":"", "value":"Number of coffees"})
        fig1.update_traces(hovertemplate='%{y}')
        fig1.update_layout(title_font_size=24, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        st.plotly_chart(fig1, use_container_width=True)

        temp1=[]
        for i in range(len(months_all)):
             temp=[]
             temp.append(months_all[i])
             temp.append(monthly_coffees_all[1][i])
             temp1.append(temp)
        
        columns=['months','total']
        df = pd.DataFrame(temp1, columns=columns)              #total coffees per month)
        fig2 = px.bar(df, y="total", x="months", title="Total number of coffees per month", labels={"months":"", "total":"Number of coffees"}, text_auto=True)
        fig2.update_layout(title_font_size=24)
        fig2.update_traces(hovertemplate='%{x}<br>%{y} coffees')
        st.plotly_chart(fig2, use_container_width=True) 

        
    #-------------------------------------------------------------------------------------------------------------- total coffees (pie chart)
    if coffees_total or all_diagrams:
        col1, col2 = st.columns([1,1])
        col1.subheader("Total coffees")

        total_coffees = get_total_coffees(names)
        
        temp=[]
        for i in range(len(total_coffees)):
            temp1=[]
            temp1.append(names)
            temp1.append(total_coffees[i])
            temp.append(temp1)
        df = pd.DataFrame(temp, columns={"names","total"}, index=names)              #total coffees pie chart

        #fig3 = px.pie(df, names = names, values = total_coffees)
        fig3 = go.Figure(go.Pie(labels = names, values = total_coffees, sort=False, hole=.4))
        fig3.update_layout(title_font_size=24)
        col1.plotly_chart(fig3, use_container_width=True)

        
    #-------------------------------------------------------------------------------------------------------------- monthly ratios (stacked bar chart)
        col2.subheader("Monthly ratios")

        monthly_ratios=get_monthly_ratio(names, month_id_all)

        months_inv=[]
        monthly_ratios_inv=[]
        for i in range(len(months_all)):
            months_inv.append(months_all[len(months_all)-i-1])
            monthly_ratios_inv.append(monthly_ratios[len(monthly_ratios)-i-1])

        df_stack=pd.DataFrame(monthly_ratios_inv, columns = names, index = months_inv)
        fig4 = px.bar(df_stack, x=names, y = months_inv, barmode = 'relative', labels={"y":"", "value":"Percentage", "variable":"drinker"})#, text='value', text_auto=True)
        fig4.update_layout(title_font_size=24, showlegend=False)
        fig4.update_traces(hovertemplate='%{y}<br>%{x} %')
        col2.plotly_chart(fig4, use_container_width=True)
        
    #-------------------------------------------------------------------------------------------------------------- expectation values and MAD (scatter chart and bar chart)
    if expectation_data:
        act_func=get_active_func()
        st.subheader("Prediction Data (active functional: "+act_func+")")
        col7,col8 = st.columns([1,1])
        
        exp_values = get_expectation_values(names, month_id_all, func_selected)
        stdev = get_stdev(names, month_id_all)
        
        max_values=[]
        for i in range(len(names)):
            if exp_values[i] < 0:
                exp_values[i] = 0
            max_values.append(exp_values[i]+stdev[i])
        
        mad_total = get_mad(names, month_id_all)
        
        df = pd.DataFrame(exp_values, columns={'Number of coffees'}, index=names)                #expectation values with standard deviation
        df["e"] = stdev

        info = act_func
        fig8 = px.scatter(df, x=names, y='Number of coffees', error_y='e', title="Expect. val.  ± σ for "+months_all[len(months_all)-1], labels={"x":"", "y":"Number of coffees", "variable":"drinkers"}, text="Number of coffees")
        fig8.update_layout(title_font_size=24, showlegend=False)
        fig8.update_traces(marker = dict(symbol = 'line-ew-open'), hovertemplate='%{x}: %{y}', textposition='middle right')
        fig8.update_yaxes(range=[0,max(max_values)+2])
        col7.plotly_chart(fig8, use_container_width=True)
        
        columns=['Functional','MAD']
        df = pd.DataFrame(mad_total, columns=columns)
        
        fig8 = px.bar(df, x='Functional', y='MAD', title="Mean absolute deviations", labels={"x":"Functional", "count":"MAD"}, text='MAD', text_auto=True).update_xaxes(categoryorder="total ascending")
        fig8.update_layout(title_font_size=24, showlegend=False)
        fig8.update_traces(hovertemplate='%{x}<br>MAD = %{y}')
        col8.plotly_chart(fig8, use_container_width=True)
           
        
        #-------------------------------------------------------------------------------------------------------------- coffee prize history (scatter + bar chart)
        st.subheader("Prize history")
        col1, col2 = st.columns([2,1])
        prizes = get_prizes(names, month_id_dly, act_func)
        
        tickval_num=[]
        total_prizes=[]
        for i in range(len(names)):
            tickval_num.append(i)
            total=0
            for j in range(len(prizes)):
                if prizes[j][1] == i:
                    total += 1
            total_prizes.append(total)

        columns=['Month','Persons','Coffee prizes','sizes']
        df = pd.DataFrame(prizes, columns=columns)

        fig2 = px.scatter(df, x='Month', y='Persons', title="Coffee prize history ("+act_func+")", labels={"variable":"", "index":"", "value":""}, size='sizes', color='Coffee prizes', color_discrete_sequence=['gold','black','red'])      #plotting social score
        fig2.update_layout(title_font_size=24, yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), hovermode="x unified", xaxis=dict(tickmode = 'array', tickvals = month_id_dly, ticktext = months_dly), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        fig2.update_traces(hovertemplate='%{y}')
        col1.plotly_chart(fig2, use_container_width=True)


        df = pd.DataFrame(total_prizes, columns={'Number of prizes'}, index=names)                #total number of prizes

        fig8 = px.bar(df, x='Number of prizes', y=names, title="Total number of prizes", labels={"y":"", "count":"Social score", "variable":"drinkers"}, text='Number of prizes', text_auto=True, orientation='h').update_yaxes(categoryorder="total ascending")
        fig8.update_layout(title_font_size=24, showlegend=False)
        fig8.update_traces(hovertemplate='%{y}: %{x}')
        fig8.update_xaxes(showticklabels=False)
        col2.plotly_chart(fig8, use_container_width=True)

        
    #-------------------------------------------------------------------------------------------------------------- weekly coffees and breaks (line chart)
    if c_b_weekly:
        st.subheader("Weekly breaks and coffees")
        columns=['Breaks','Coffees']
        weekly_data = get_weekly_coffees_breaks(names)

        weeks=[]
        weekly_br_c=[]
    
        for i in range(len(weekly_data)):
            temp=[]
            weeks.append(weekly_data[i][0])
            temp.append(weekly_data[i][1])
            temp.append(weekly_data[i][2])
            weekly_br_c.append(temp)

        df = pd.DataFrame(weekly_br_c, columns=columns, index=weeks)              #weekly coffees/breaks

        fig3 = px.line(df, title="Weekly coffee breaks and coffees", labels={"variable":"", "index":"", "value":""})
        fig3.update_layout(title_font_size=24, hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        fig3.update_traces(hovertemplate='%{y}')
        st.plotly_chart(fig3, use_container_width=True)


    #-------------------------------------------------------------------------------------------------------------- absolute and relative correlations (bubble charts)
    if correlation:
        st.subheader("Correlation diagrams")
        col3, col4 = st.columns([1,1])                        #setting up two columns for narrower charts        
        corr_tot=get_correlation(names)
        corr_abs_raw=corr_tot[0]
        corr_rel_raw=corr_tot[1]
        print(corr_tot)
        temp1=[]
        temp2_abs=[]
        temp2_rel=[]
        tickval_num=[]
        names_inv=[]
        for i in range(len(names)):
            tickval_num.append(i+1)
            names_inv.append(names[len(names)-i-1])
            for j in range(len(names)):
               temp_abs=[]
               temp_rel=[]
               temp_abs.append(i+1)
               temp_rel.append(i+1)
               temp_abs.append(j+1)
               temp_rel.append(j+1)
               #temp_abs.append(corr_abs_raw[len(names)-j-1][i])      #calculates absolute correlation
               #temp_rel.append(corr_rel_raw[len(names)-j-1][i])      #calculates relative correlation
               temp_abs.append(corr_abs_raw[i][len(names)-j-1])      #calculates absolute correlation
               temp_rel.append(corr_rel_raw[i][len(names)-j-1])      #calculates relative correlation
               temp2_abs.append(temp_abs)
               temp2_rel.append(temp_rel)
        columns_corr_abs=['x-values','y-values','Coffees']
        columns_corr_rel=['x-values','y-values','Percent']
        
        df = pd.DataFrame(temp2_abs, columns=columns_corr_abs)
        fig5 = px.scatter(df, x='x-values', y='y-values', size='Coffees', custom_data=['Coffees'], labels={"x-values":"", "y-values":""}, title="Absolute correlation", color='Coffees')
        fig5.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
        #fig5.update_traces(hovertemplate="%{y} with %{x}:<br>%{customdata[0]} coffees")
        fig5.update_traces(hovertemplate="%{y} drank %{customdata[0]} coffees with %{x}")
        fig5.update_xaxes(side="top")
        col3.plotly_chart(fig5, use_container_width=True)#              absolute correlation
        #                                                  --------------------------------------------------
        df = pd.DataFrame(temp2_rel, columns=columns_corr_rel)
        fig6 = px.scatter(df, x='x-values', y='y-values', size='Percent', custom_data=['Percent'], labels={"x-values":"", "y-values":""}, title="Relative correlation", color='Percent')#, text='size')
        fig6.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
        #fig6.update_traces(hovertemplate="%{x} with %{y}:<br>%{customdata[0]} %")
        fig6.update_traces(hovertemplate="%{y} drank %{customdata[0]} % of<br>their coffees with %{x}")
        fig6.update_xaxes(side="top")
        col4.plotly_chart(fig6, use_container_width=True)
        
        
        
        
        
        
