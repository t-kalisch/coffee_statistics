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
if 'logged_in' not in st.session_state or 'user_name' not in st.session_state or 'admin' not in st.session_state or 'attempt' not in st.session_state:
    st.warning("Warning! Your session was terminated due to inactivity. Please return to home to restart it and regain access to all features.")
else:
  
  #simple_data=get_simple_data()
  simple_data = [[17],[6],[37],[1600],[4860],[148],[18]]            #last values before closing server
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
      #all_func = get_functionals()
      all_func = ["BS3LYP","BS3LYPp","dynamic","dynamicp","KKBK21","KKBK21-G2","KKBK21-G2I","PBTK","PJGL21","polypony","TKPBW95","TKPBW95p"]            #last values before closing server
      with st.sidebar:
          #act_func = get_active_func()
          act_func = "dynamicp"             #last values before closing server
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
          #all_diagrams_new = st.checkbox("Show all new")
          all_diagrams = st.checkbox("Show all")
          coffees_monthly = st.checkbox("Monthly coffees")
          coffees_total = st.checkbox("Total coffees / Monthly ratios")
          expectation_data = st.checkbox("Expectation values / Prize history")
          c_b_weekly = st.checkbox ("Weekly data")
          correlation = st.checkbox("Correlation")
          break_percentage = st.checkbox("Percentages of breaks")
          soc_sc = st.checkbox("Social score")
          coffees_pwd = st.checkbox("Coffees per work day")
          coffees_cumulated = st.checkbox("Cumulated coffees")  

          if st.session_state.admin == "1":
              update = st.button("Update", help="Update database", on_click=update_database)

      #names = get_members()
      names = ["TK","PB","NV","DB","FLG","SHK","TB","TT","RS","VB","MR","KKM","SB","SK","AK","GP","DM"]           #last values before closing server
      #month_info=get_months(datetime.date(2021,3,8))    #start of daily records
      month_info = [["Mar '21","Apr '21","May '21","Jun '21","Jul '21","Aug '21","Sep '21","Oct '21","Nov '21","Dec '21","Jan '22","Feb '22","Mar '22","Apr '22","May '22","Jun '22","Jul '22","Aug '22","Sep '22","Oct '22","Nov '22","Dec '22","Jan '23","Feb '23","Mar '23","Apr '23","May '23","Jun '23","Jul '23","Aug '23","Sep '23","Oct '23","Nov '23","Dec '23"],
                    ["202103","202104","202105","202106","202107","202108","202109","202110","202111","202112","202201","202202","202203","202204","202205","202206","202207","202208","202209","202210","202211","202212","202301","202302","202303","202304","202305","202306","202307","202308","202309","202310","202311","202312"]]           #last values before closing server
      months_dly=month_info[0]
      month_id_dly=month_info[1]
      #month_info=get_months(datetime.date(2020,11,1))    #start of monthly records
      month_info = [["Nov'20","Dec'20","Jan'21","Feb'21","Mar'21","Apr'21","May'21","Jun'21","Jul'21","Aug'21","Sep'21","Oct'21","Nov'21","Dec'21","Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'23","Feb'23","Mar'23","Apr'23","May'23","Jun'23","Jul'23","Aug'23","Sep'23","Oct'23","Nov'23","Dec'23"],
                    ["202011","202012","202101","202102","202103","202104","202105","202106","202107","202108","202109","202110","202111","202112","202201","202202","202203","202204","202205","202206","202207","202208","202209","202210","202211","202212","202301","202302","202303","202304","202305","202306","202307","202308","202309","202310","202311","202312"]]           #last values before closing server
      months_all=month_info[0]
      month_id_all=month_info[1]

      #--------------------- show all diagrams ------------------------------ 
      #if all_diagrams_new:
      #  ssh = paramiko.SSHClient()
      #  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      #  ssh.connect(**st.secrets["ssh-server"])
      #  
      #  stdin, stdout, stderr = ssh.exec_command("cd ../home; python3 get_all_data.py '"+func_selected+"' '"+"032021"+"' '"+"102022"+"'")
      #  all_data_str = stdout.readlines()
      #  
      #  all_data = [ x.strip() for x in all_data_str[0].split('|') ]
      #  st.write(all_data)

        
      #  # coffees per month
      #  st.subheader("Coffees per month") 
      #  monthly_coffees_all = [ x.strip() for x in all_data[0].strip(';').split(';') ]
      #  
      #  for i in range(len(monthly_coffees_all)):
      #    if '_' in monthly_coffees_all[i]:
      #      monthly_coffees_all[i] = [ x.strip() for x in monthly_coffees_all[i].strip('_').split('_') ]
      #    st.write(monthly_coffees_all)
      #    for j in range(len(monthly_coffees_all[i])):
      #       if ',' in monthly_coffees_all[i][j]:
      #         monthly_coffees_all[i][j] = [ x.strip() for x in monthly_coffees_all[i][j].strip(',').split(',') ]


      #  st.write(monthly_coffees_all)
        
      #  df = pd.DataFrame(monthly_coffees_all[0], columns=names, index=months_all)    #coffees per month per person

      #  fig1 = px.line(df, title="Number of coffees per month per person", labels={"variable":"", "index":"", "value":"Number of coffees"})
      #  fig1.update_traces(hovertemplate='%{y}')
      #  fig1.update_layout(title_font_size=24, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
      #  st.plotly_chart(fig1, use_container_width=True)

      #  temp1=[]
      #  for i in range(len(months_all)):
      #       temp=[]
      #       temp.append(months_all[i])
      #       temp.append(monthly_coffees_all[1][i])
      #       temp1.append(temp)

      #  columns=['months','total']
      #  df = pd.DataFrame(temp1, columns=columns)              #total coffees per month)
      #  fig2 = px.bar(df, y="total", x="months", title="Total number of coffees per month", labels={"months":"", "total":"Number of coffees"}, text_auto=True)
      #  fig2.update_layout(title_font_size=24)
      #  fig2.update_traces(hovertemplate='%{x}<br>%{y} coffees')
      #  st.plotly_chart(fig2, use_container_width=True) 
        
        
        
        
      #else:
      #-------------------------------------------------------------------------------------------------------------- monthly coffees, per person + total (line + bar chart)
      if coffees_monthly or all_diagrams:
          st.subheader("Coffees per month") 

          #monthly_coffees_all = get_monthly_coffees(names, month_id_all)        #sorted by month, not by name!
          monthly_coffees_all = [[[19,15,13,10,18,0,0,0,0,0,0,0,0,0,0,0,0],           #last values before closing server
                                  [9,6,6,3,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [16,6,12,7,18,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [19,20,16,12,21,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [29,29,25,27,34,19,0,0,0,0,0,0,0,0,0,0,0],
                                  [31,20,35,36,35,27,12,0,0,0,0,0,0,0,0,0,0],
                                  [32,24,28,37,35,23,18,0,0,0,0,0,0,0,0,0,0],
                                  [30,25,37,15,26,9,8,0,0,0,0,0,0,0,0,0,0],
                                  [14,29,31,22,21,5,5,0,0,0,0,0,0,0,0,0,0],
                                  [41,22,27,44,43,16,13,0,0,0,0,0,0,0,0,0,0],
                                  [39,32,36,10,43,22,2,0,0,0,0,0,0,0,0,0,0],
                                  [33,30,30,6,27,17,0,0,0,0,0,0,0,0,0,0,0],
                                  [37,35,22,4,36,26,0,0,3,0,0,0,0,0,0,0,0],
                                  [24,18,14,7,22,17,0,1,0,0,0,0,0,0,0,0,0],
                                  [29,31,3,1,24,16,0,0,1,0,0,0,0,0,0,0,0],
                                  [35,36,1,18,36,31,0,1,0,1,0,0,0,0,0,0,0],
                                  [50,46,2,62,56,42,0,0,0,0,2,0,0,0,0,0,0],
                                  [39,40,0,47,49,30,0,1,3,0,0,0,0,0,0,0,0],
                                  [22,33,1,36,41,22,0,1,2,0,1,0,0,0,0,0,0],
                                  [9,8,0,17,44,19,0,0,2,0,0,0,0,0,0,0,0],
                                  [11,9,0,7,1,16,0,1,2,0,0,0,0,0,0,0,0],
                                  [26,22,0,3,32,4,0,0,0,0,0,3,0,0,0,0,0],
                                  [30,34,0,33,19,4,1,0,1,0,0,0,0,0,0,0,0],
                                  [39,33,0,4,35,7,2,0,3,0,0,0,1,0,0,0,0],
                                  [47,36,0,23,38,14,2,0,2,0,0,0,4,8,0,0,0],
                                  [32,20,0,16,35,7,1,0,0,1,1,0,0,0,0,0,0],
                                  [38,38,0,9,23,21,0,0,0,0,1,0,0,0,0,0,0],
                                  [39,42,0,20,41,15,0,0,0,0,0,0,0,0,0,0,0],
                                  [32,36,0,28,41,4,0,0,0,0,2,0,0,0,0,0,0],
                                  [42,21,2,49,43,0,1,2,2,0,2,0,0,0,0,0,0],
                                  [37,14,0,6,53,1,0,0,1,0,0,0,0,0,0,0,0],
                                  [39,0,0,2,39,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [20,21,0,0,39,0,0,0,1,0,0,0,0,0,2,7,4],
                                  [30,12,0,0,46,0,0,0,0,0,1,0,0,0,1,2,2],
                                  [29,32,0,0,38,0,1,1,0,0,0,0,3,0,2,9,5],
                                  [33,23,0,0,33,0,1,1,0,0,1,0,0,0,3,9,6],
                                  [11,14,0,0,34,0,0,0,0,0,0,0,0,0,2,3,3],
                                  [10,11,0,0,23,0,0,0,0,0,0,0,0,0,0,4,1]],
                                  [75,25,59,88,163,196,197,150,127,206,184,143,163,103,105,159,260,209,159,99,47,90,122,124,174,113,130,157,143,164,112,80,94,94,120,110,67,49]]


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

          #total_coffees = get_total_coffees(names)
          total_coffees = [1102,923,341,621,1243,434,67,9,23,2,11,3,8,8,10,34,21]           #last values before closing server
          temp=[]
          for i in range(len(total_coffees)):
              temp1=[]
              temp1.append(names[i])
              temp1.append(total_coffees[i])
              temp.append(temp1)

          columns=["names","total"]
          df = pd.DataFrame(temp, columns=columns, index=names)              #total coffees pie chart

          #fig3 = px.pie(df, names = names, values = total_coffees)
          fig3 = go.Figure(go.Pie(labels = names, values = total_coffees, sort=False, hole=.4))
          fig3.update_layout(title="Total percentage of coffees", title_font_size=24)
          col1.plotly_chart(fig3, use_container_width=True)


      #-------------------------------------------------------------------------------------------------------------- monthly ratios (stacked bar chart)
          col2.subheader("Monthly ratios")

          #monthly_ratios=get_monthly_ratio(names, month_id_all)
          monthly_ratios = [[25.333333333333332,20,17.333333333333332,13.333333333333334,24,0,0,0,0,0,0,0,0,0,0,0,0],           #last values before closing server
                            [36,24,24,12,4,0,0,0,0,0,0,0,0,0,0,0,0],
                            [27.11864406779661,10.169491525423728,20.338983050847457,11.864406779661017,30.508474576271187,0,0,0,0,0,0,0,0,0,0,0,0],
                            [21.59090909090909,22.727272727272727,18.181818181818183,13.636363636363637,23.863636363636363,0,0,0,0,0,0,0,0,0,0,0,0],
                            [17.791411042944784,17.791411042944784,15.337423312883436,16.56441717791411,20.858895705521473,11.656441717791411,0,0,0,0,0,0,0,0,0,0,0],
                            [15.816326530612244,10.204081632653061,17.857142857142858,18.367346938775512,17.857142857142858,13.775510204081632,6.122448979591836,0,0,0,0,0,0,0,0,0,0],
                            [16.243654822335024,12.182741116751268,14.213197969543147,18.781725888324875,17.766497461928935,11.6751269035533,9.137055837563452,0,0,0,0,0,0,0,0,0,0],
                            [20,16.666666666666668,24.666666666666668,10,17.333333333333332,6,5.333333333333333,0,0,0,0,0,0,0,0,0,0],
                            [11.023622047244094,22.834645669291337,24.409448818897637,17.322834645669293,16.53543307086614,3.937007874015748,3.937007874015748,0,0,0,0,0,0,0,0,0,0],
                            [19.902912621359224,10.679611650485437,13.106796116504855,21.359223300970875,20.87378640776699,7.766990291262136,6.310679611650485,0,0,0,0,0,0,0,0,0,0],
                            [21.195652173913043,17.391304347826086,19.565217391304348,5.434782608695652,23.369565217391305,11.956521739130435,1.0869565217391304,0,0,0,0,0,0,0,0,0,0],
                            [23.076923076923077,20.97902097902098,20.97902097902098,4.195804195804196,18.88111888111888,11.888111888111888,0,0,0,0,0,0,0,0,0,0,0],
                            [22.699386503067483,21.47239263803681,13.496932515337424,2.4539877300613497,22.085889570552148,15.950920245398773,0,0,1.8404907975460123,0,0,0,0,0,0,0,0],
                            [23.300970873786408,17.475728155339805,13.592233009708737,6.796116504854369,21.359223300970875,16.50485436893204,0,0.970873786407767,0,0,0,0,0,0,0,0,0],
                            [27.61904761904762,29.523809523809526,2.857142857142857,0.9523809523809523,22.857142857142858,15.238095238095237,0,0,0.9523809523809523,0,0,0,0,0,0,0,0],
                            [22.0125786163522,22.641509433962263,0.6289308176100629,11.320754716981131,22.641509433962263,19.49685534591195,0,0.6289308176100629,0,0.6289308176100629,0,0,0,0,0,0,0],
                            [19.23076923076923,17.692307692307693,0.7692307692307693,23.846153846153847,21.53846153846154,16.153846153846153,0,0,0,0,0.7692307692307693,0,0,0,0,0,0],
                            [18.660287081339714,19.138755980861244,0,22.48803827751196,23.444976076555022,14.354066985645932,0,0.4784688995215311,1.4354066985645932,0,0,0,0,0,0,0,0],
                            [13.836477987421384,20.754716981132077,0.6289308176100629,22.641509433962263,25.78616352201258,13.836477987421384,0,0.6289308176100629,1.2578616352201257,0,0.6289308176100629,0,0,0,0,0,0],
                            [9.090909090909092,8.080808080808081,0,17.171717171717173,44.44444444444444,19.19191919191919,0,0,2.0202020202020203,0,0,0,0,0,0,0,0],
                            [23.404255319148938,19.148936170212767,0,14.893617021276595,2.127659574468085,34.04255319148936,0,2.127659574468085,4.25531914893617,0,0,0,0,0,0,0,0],
                            [28.88888888888889,24.444444444444443,0,3.3333333333333335,35.55555555555556,4.444444444444445,0,0,0,0,0,3.3333333333333335,0,0,0,0,0],
                            [24.59016393442623,27.868852459016395,0,27.049180327868854,15.573770491803279,3.278688524590164,0.819672131147541,0,0.819672131147541,0,0,0,0,0,0,0,0],
                            [31.451612903225808,26.612903225806452,0,3.225806451612903,28.225806451612904,5.645161290322581,1.6129032258064515,0,2.4193548387096775,0,0,0,0.8064516129032258,0,0,0,0],
                            [27.011494252873565,20.689655172413794,0,13.218390804597702,21.839080459770116,8.045977011494253,1.1494252873563218,0,1.1494252873563218,0,0,0,2.2988505747126435,4.597701149425287,0,0,0],
                            [28.31858407079646,17.699115044247787,0,14.15929203539823,30.97345132743363,6.1946902654867255,0.8849557522123894,0,0,0.8849557522123894,0.8849557522123894,0,0,0,0,0,0],
                            [29.23076923076923,29.23076923076923,0,6.923076923076923,17.692307692307693,16.153846153846153,0,0,0,0,0.7692307692307693,0,0,0,0,0,0],
                            [24.840764331210192,26.751592356687897,0,12.738853503184714,26.11464968152866,9.554140127388536,0,0,0,0,0,0,0,0,0,0,0],
                            [22.377622377622377,25.174825174825173,0,19.58041958041958,28.67132867132867,2.797202797202797,0,0,0,0,1.3986013986013985,0,0,0,0,0,0],
                            [25.609756097560975,12.804878048780488,1.2195121951219512,29.878048780487806,26.21951219512195,0,0.6097560975609756,1.2195121951219512,1.2195121951219512,0,1.2195121951219512,0,0,0,0,0,0],
                            [33.035714285714285,12.5,0,5.357142857142857,47.32142857142857,0.8928571428571429,0,0,0.8928571428571429,0,0,0,0,0,0,0,0],
                            [48.75,0,0,2.5,48.75,0,0,0,0,0,0,0,0,0,0,0,0],
                            [21.27659574468085,22.340425531914892,0,0,41.48936170212766,0,0,0,1.0638297872340425,0,0,0,0,0,2.127659574468085,7.446808510638298,4.25531914893617],
                            [31.914893617021278,12.76595744680851,0,0,48.93617021276596,0,0,0,0,0,1.0638297872340425,0,0,0,1.0638297872340425,2.127659574468085,2.127659574468085],
                            [24.166666666666668,26.666666666666668,0,0,31.666666666666668,0,0.8333333333333334,0.8333333333333334,0,0,0,0,2.5,0,1.6666666666666667,7.5,4.166666666666667],
                            [30,20.90909090909091,0,0,30,0,0.9090909090909091,0.9090909090909091,0,0,0.9090909090909091,0,0,0,2.727272727272727,8.181818181818182,5.454545454545454],
                            [16.417910447761194,20.895522388059703,0,0,50.74626865671642,0,0,0,0,0,0,0,0,0,2.985074626865672,4.477611940298507,4.477611940298507],
                            [20.408163265306122,22.448979591836736,0,0,46.93877551020408,0,0,0,0,0,0,0,0,0,0,8.16326530612245,2.0408163265306123]]


          months_inv=[]
          monthly_ratios_inv=[]
          for i in range(len(months_all)):
              months_inv.append(months_all[len(months_all)-i-1])
              monthly_ratios_inv.append(monthly_ratios[len(monthly_ratios)-i-1])

          df_stack=pd.DataFrame(monthly_ratios_inv, columns = names, index = months_inv)
          fig4 = px.bar(df_stack, x=names, y = months_inv, barmode = 'relative', title="Monthly percentage of coffees", labels={"y":"", "value":"Percentage", "variable":"drinker"})#, text='value', text_auto=True)
          fig4.update_layout(title_font_size=24, showlegend=False)
          fig4.update_traces(hovertemplate='%{y}<br>%{x} %')
          col2.plotly_chart(fig4, use_container_width=True)

      #-------------------------------------------------------------------------------------------------------------- expectation values and MAD (scatter chart and bar chart)
      if expectation_data or all_diagrams:
          act_func=get_active_func()
          st.subheader("Prediction Data (active functional: "+act_func+")")
          col7,col8 = st.columns([1,1])

          exp_values = get_expectation_values(names, month_id_all, func_selected)
          st.write(exp_values)
          stdev = get_stdev(names, month_id_all)

          max_values=[]
          for i in range(len(names)):
              if exp_values[i] < 0:
                  exp_values[i] = 0
              max_values.append(exp_values[i]+stdev[i])

          mad_total = get_mad(names, month_id_all)

          columns=['Number of coffees']
          df = pd.DataFrame(exp_values, columns=columns, index=names)                #expectation values with standard deviation
          df["e"] = stdev

          info = act_func
          fig8 = px.scatter(df, x=names, y='Number of coffees', error_y='e', title="Expect. values  ± σ for "+months_all[len(months_all)-1], labels={"x":"", "y":"Number of coffees", "variable":"drinkers"}, text="Number of coffees")
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
          month_numbers = []
          tmp = 0
          for i in range(len(prizes)):
              if i % 3 == 0:
                  tmp += 1
                  month_numbers.append(tmp)
              prizes[i][0]=str(tmp)
          
          tickval_num=[]
          total_prizes=[]

          prizes_search=["Kaffeemeister","Hotshot","Genosse"]
          for i in range(len(names)):
              tickval_num.append(i)
              km=0
              hs=0
              gn=0
              temp=[]
              for j in range(3):
                  temp=[]
                  temp.append(names[i])
                  temp.append(prizes_search[j])
                  total=0
                  for k in range(len(prizes)):
                      if prizes[k][1] == i and prizes[k][2] == prizes_search[j]:
                              total += 1
                  temp.append(total)
                  if j == 2:
                      sum = (int(total_prizes[len(total_prizes)-2][2]+total_prizes[len(total_prizes)-1][2]+total))
                      if temp[2] == 0:
                          if total_prizes[len(total_prizes)-1][2] == 0:
                              total_prizes[len(total_prizes)-2].append(sum)
                          else:
                              total_prizes[len(total_prizes)-1].append(sum)
                      else:
                          temp.append(sum)
                  total_prizes.append(temp)
          

          columns=['Month','Persons','Coffee prizes','sizes']
          df = pd.DataFrame(prizes, columns=columns)

          fig2 = px.scatter(df, x='Month', y='Persons', title="Coffee prize history ("+act_func+")", labels={"variable":"", "index":"", "value":""}, size='sizes', color='Coffee prizes', color_discrete_sequence=['gold','black','red']) 
          fig2.update_layout(title_font_size=24, yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), hovermode="x unified", xaxis=dict(tickmode = 'array', tickvals = month_numbers, ticktext = months_dly), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig2.update_traces(hovertemplate='%{y}')
          col1.plotly_chart(fig2, use_container_width=True)


          columns=['Persons','prize','Number of prizes','total']
          df = pd.DataFrame(total_prizes, columns=columns)                #total number of prizes

          fig8 = px.bar(df, x='Number of prizes', y='Persons', title="Total number of prizes", labels={"y":"", "count":"Social score", "variable":"drinkers"}, color="prize", color_discrete_sequence=['gold','black','red'], text='total', orientation='h').update_yaxes(categoryorder="total ascending")
          fig8.update_layout(title_font_size=24, showlegend=False, hovermode="y unified")
          fig8.update_traces(hovertemplate='%{x}')
          fig8.update_xaxes(showticklabels=False)
          col2.plotly_chart(fig8, use_container_width=True)


      #-------------------------------------------------------------------------------------------------------------- weekly coffees and breaks (line chart)
      if c_b_weekly or all_diagrams:
          st.subheader("Weekly breaks, coffees and average break sizes")
          columns=['Breaks','Coffees','Average break size']
          weekly_data = get_weekly_coffees_breaks(names)

          weeks=[]
          weekly_br_c=[]
          avg_br_size=[] 
          
          for i in range(len(weekly_data)):
              temp=[]
              weeks.append(weekly_data[i][0])
              temp.append(weekly_data[i][1])
              temp.append(weekly_data[i][2])
              #if weekly_data[i][3] == Null:
              #    temp.append(float(0))
              #else:
              temp.append(float(weekly_data[i][3]))
              weekly_br_c.append(temp)

          df = pd.DataFrame(weekly_br_c, columns=columns, index=weeks)              #weekly coffees/breaks
          fig3 = px.line(df, title="Weekly data", labels={"variable":"", "index":"", "value":""}, color_discrete_sequence=['#636EFA','#EF553B','grey'])
          fig3.update_layout(title_font_size=24, hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig3.update_traces(hovertemplate='%{y}')
          st.plotly_chart(fig3, use_container_width=True)


      #-------------------------------------------------------------------------------------------------------------- absolute and relative correlations (bubble charts)
      if correlation or all_diagrams:
          #st.subheader("Correlation diagrams")
          
          
          #colorscales = px.colors.named_colorscales()
          #st.write(colorscales)
          
          #scale = st.selectbox("select color scheme",colorscales)
          
          
         # col3, col4 = st.columns([1,1])                        #setting up two columns for narrower charts        
         # corr_tot=get_correlation(names)
         # corr_abs_raw=corr_tot[0]
         # corr_rel_raw=corr_tot[1]
         # 
         # temp1=[]
         # temp2_abs=[]
         # temp2_rel=[]
         # tickval_num=[]
         # names_inv=[]
         # for i in range(len(names)):
         #     tickval_num.append(i+1)
         #     names_inv.append(names[len(names)-i-1])
         #     for j in range(len(names)):
         #        temp_abs=[]
         #        temp_rel=[]
         #        temp_abs.append(i+1)
         #        temp_rel.append(i+1)
         #        temp_abs.append(j+1)
         #        temp_rel.append(j+1)
         #        #temp_abs.append(corr_abs_raw[len(names)-j-1][i])      #calculates absolute correlation
         #        #temp_rel.append(corr_rel_raw[len(names)-j-1][i])      #calculates relative correlation
         #        temp_abs.append(corr_abs_raw[i][len(names)-j-1])      #calculates absolute correlation
         #        temp_rel.append(corr_rel_raw[i][len(names)-j-1])      #calculates relative correlation
         #        temp2_abs.append(temp_abs)
         #        temp2_rel.append(temp_rel)
         # columns_corr_abs=['x-values','y-values','Coffees']
         # columns_corr_rel=['x-values','y-values','Percent']

         # df = pd.DataFrame(temp2_abs, columns=columns_corr_abs)
         # fig5 = px.scatter(df, x='x-values', y='y-values', size='Coffees', custom_data=['Coffees'], labels={"x-values":"", "y-values":""}, title="Absolute correlation", color='Coffees')
         # fig5.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
         # #fig5.update_traces(hovertemplate="%{y} with %{x}:<br>%{customdata[0]} coffees")
         # fig5.update_traces(hovertemplate="%{y} drank %{customdata[0]} coffees with %{x}")
         # fig5.update_xaxes(side="top")
         # col3.plotly_chart(fig5, use_container_width=True)#              absolute correlation
         # #                                                  --------------------------------------------------
         # df = pd.DataFrame(temp2_rel, columns=columns_corr_rel)
         # fig6 = px.scatter(df, x='x-values', y='y-values', size='Percent', custom_data=['Percent'], labels={"x-values":"", "y-values":""}, title="Relative correlation", color='Percent')#, text='size')
         # fig6.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
         # #fig6.update_traces(hovertemplate="%{x} with %{y}:<br>%{customdata[0]} %")
         # fig6.update_traces(hovertemplate="%{y} drank %{customdata[0]} % of<br>their coffees with %{x}")
         # fig6.update_xaxes(side="top")
         # col4.plotly_chart(fig6, use_container_width=True)


          #--------------------------------- time resolved correlation data ------------------------------------
          scale = "portland"
          timespan = st.slider("Timespan for correlation", min_value=datetime.date(2021,3,1), max_value=datetime.date.today(), value=(datetime.date(2021, 3, 1), datetime.date.today()), format="MM/YYYY")
          month_start = str(timespan[0].year)
          if timespan[0].month < 10:
              month_start += "0"+str(timespan[0].month)
          else:
              month_start += str(timespan[0].month)
          month_end = str(timespan[1].year)
          if timespan[1].month < 10:
              month_end += "0"+str(timespan[1].month)
          else:
              month_end += str(timespan[1].month)

          corr_tot_time = get_corr_time(names, month_start, month_end)
          corr_abs_raw=corr_tot_time[0]
          corr_rel_raw=corr_tot_time[1]

          col3, col4 = st.columns([1,1])                        #setting up two columns for narrower charts
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
                 temp_abs.append(corr_abs_raw[len(names)-j-1][i])      #calculates absolute correlation
                 #temp_rel.append(corr_rel_raw[len(names)-j-1][i])      #calculates relative correlation
                 #temp_abs.append(corr_abs_raw[i][len(names)-j-1])      #calculates absolute correlation
                 temp_rel.append(corr_rel_raw[i][len(names)-j-1])      #calculates relative correlation
                 temp2_abs.append(temp_abs)
                 temp2_rel.append(temp_rel)
          columns_corr_abs=['x-values','y-values','Coffees']
          columns_corr_rel=['x-values','y-values','Percent']

          df = pd.DataFrame(temp2_abs, columns=columns_corr_abs)
          fig11 = px.scatter(df, x='x-values', y='y-values', size='Coffees', custom_data=['Coffees'], labels={"x-values":"", "y-values":""}, title="Absolute correlation", color='Coffees', color_continuous_scale=scale)
          fig11.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
          #fig5.update_traces(hovertemplate="%{y} with %{x}:<br>%{customdata[0]} coffees")
          fig11.update_traces(hovertemplate="%{y} drank %{customdata[0]} coffees with %{x}")
          fig11.update_xaxes(side="top")
          col3.plotly_chart(fig11, use_container_width=True)#              absolute correlation
          #                                                  --------------------------------------------------
          df = pd.DataFrame(temp2_rel, columns=columns_corr_rel)
          fig12 = px.scatter(df, x='x-values', y='y-values', size='Percent', custom_data=['Percent'], labels={"x-values":"", "y-values":""}, title="Relative correlation", color='Percent', color_continuous_scale=scale)#, text='size')
          fig12.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names_inv))
          #fig6.update_traces(hovertemplate="%{x} with %{y}:<br>%{customdata[0]} %")
          fig12.update_traces(hovertemplate="%{y} drank %{customdata[0]} % of<br>their coffees with %{x}")
          fig12.update_xaxes(side="top")
          col4.plotly_chart(fig12, use_container_width=True)

     #-------------------------------------------------------------------------------------------------------------- percentages of breaks (line + bar charts)
      if break_percentage or all_diagrams:
          st.subheader("Percentages of breaks")
          col5,col6 = st.columns([2,1])

          percentages=get_perc_breaks(names, month_id_dly)
          percentage_total=percentages[0]
          percentage=[]
          for i in range(len(percentages)-1):
              percentage.append(percentages[i+1])

          df = pd.DataFrame(percentage, columns=names, index=months_dly)
          fig7 = px.line(df, title="Monthly percentages of breaks", labels={"variable":"", "index":"", "value":"Percentage"})
          fig7.update_layout(title_font_size=24, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig7.update_traces(hovertemplate='%{x}<br>%{y} %')
          col5.plotly_chart(fig7, use_container_width=True)

          columns=['percentage']
          df = pd.DataFrame(percentage_total, columns=columns, index=names)

          fig8 = px.bar(df, x='percentage', y=names, title="Total percentages of breaks", labels={"y":"", "count":"Percentage", "variable":"drinkers"}, text='percentage', text_auto=True, orientation='h').update_yaxes(categoryorder="total ascending")
          fig8.update_layout(title_font_size=24, showlegend=False)
          fig8.update_traces(hovertemplate='%{y}: %{x} %')
          col6.plotly_chart(fig8, use_container_width=True)

      #-------------------------------------------------------------------------------------------------------------- social score (line chart + bar chart)
      if soc_sc or all_diagrams:
          st.subheader("Social Score")
          col7,col8 = st.columns([2,1])

          socialscore_total = get_social_score(names, month_id_dly)
          total = socialscore_total[0]
          socialscore=[]
          #for i in range(len(socialscore_total[1])):
          #    socialscore.append(socialscore_total[1][i])

          df = pd.DataFrame(socialscore_total[1], columns=names, index=months_dly)                 #data frame for social score

          fig2 = px.line(df, title="Monthly social scores", labels={"variable":"", "index":"", "value":"Social score / a.u."})      #plotting social score
          fig2.update_layout(title_font_size=24, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig2.update_traces(hovertemplate='%{x}<br>%{y}')
          fig2.update_yaxes(showticklabels=False)
          col7.plotly_chart(fig2, use_container_width=True)

          columns=['Social score']
          df = pd.DataFrame(total, columns=columns, index=names)                #total social score

          fig8 = px.bar(df, x='Social score', y=names, title="Total social score", labels={"y":"", "count":"Social score", "variable":"drinkers"}, text='Social score', text_auto=True, orientation='h').update_yaxes(categoryorder="total ascending")
          fig8.update_layout(title_font_size=24, showlegend=False)
          fig8.update_traces(hovertemplate='%{y}: %{x} %')
          fig8.update_xaxes(showticklabels=False,range=[0,100])
          col8.plotly_chart(fig8, use_container_width=True)          


      #-------------------------------------------------------------------------------------------------------------- coffees per work day (line chart + bar chart)
      if coffees_pwd or all_diagrams:
          st.subheader("Coffees per work day")
          col7,col8 = st.columns([2,1])

          total_cpwd = get_coffees_per_work_day(names, month_id_all)
          total = total_cpwd[0]
          coffees_per_work_day = total_cpwd[1]

          df = pd.DataFrame(coffees_per_work_day, columns = names, index = months_all)

          fig9 = px.line(df, title="Monthly coffees per work day", labels={"variable":"", "index":"", "value":"Number of coffees"})      #plotting monthly coffees
          fig9.update_layout(title_font_size=24, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig9.update_traces(hovertemplate='%{x}<br>%{y}')
          col7.plotly_chart(fig9, use_container_width=True)

          columns=['Number of coffees']
          df = pd.DataFrame(total, columns=columns, index=names)                #total percentages

          fig11 = px.bar(df, x='Number of coffees', y=names, title="Total coffees per work day", labels={"y":"", "count":"Number of coffees", "variable":"drinkers"}, text='Number of coffees', text_auto=True, orientation='h').update_yaxes(categoryorder="total ascending")
          fig11.update_layout(title_font_size=24, showlegend=False)
          fig11.update_traces(hovertemplate='%{y}: %{x}')
          col8.plotly_chart(fig11, use_container_width=True)


      #-------------------------------------------------------------------------------------------------------------- cumulated coffees monthly (line chart)
      if coffees_cumulated or all_diagrams:
          st.subheader("Cumulated coffees")

          cumulated_coffees = get_cumulated_coffees(names, month_id_all)
          df = pd.DataFrame(cumulated_coffees, columns=names, index=months_all)

          fig10 = px.line(df, title="Number of coffees per month per person", labels={"variable":"", "index":"", "value":"Number of coffees"})
          fig10.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
          fig10.update_traces(hovertemplate='%{x}<br> %{y}')
          st.plotly_chart(fig10, use_container_width=True)        

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
