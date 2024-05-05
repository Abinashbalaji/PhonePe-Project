import streamlit as st
import pandas as pd
import mysql.connector
import plotly_express as px
import json
import requests


mydb = mysql.connector.connect(

  host="localhost",
  user="root",
  password="",
  database='PhonePe'

)
mycursor=mydb.cursor(buffered=True)

mycursor.execute("SELECT * FROM aggregate_trans")
mydb.commit()
tab_1 = mycursor.fetchall()
Agg_Trans = pd.DataFrame(tab_1, columns = ("State","Year","Quater","Transaction_type","Transaction_count","Transaction_amount"))


mycursor.execute("SELECT * FROM aggregate_user")
mydb.commit()
tab_2 = mycursor.fetchall()
Agg_User = pd.DataFrame(tab_2, columns = ("State","Year","Quater","brand","count","percentage"))


mycursor.execute("SELECT * FROM map_transaction")
mydb.commit()
tab_3 = mycursor.fetchall()
Map_Trans = pd.DataFrame(tab_3, columns = ("State","Year","Quater","Transaction_count","Transaction_amount"))


mycursor.execute("SELECT * FROM map_user")
mydb.commit()
tab_4 = mycursor.fetchall()
Map_User = pd.DataFrame(tab_4, columns = ("State","Year","Quater","Districts","Appopens","Registered_Users"))


mycursor.execute("SELECT * FROM top_trans")
mydb.commit()
tab_5 = mycursor.fetchall()
Top_Trans = pd.DataFrame(tab_5, columns = ("State","Year","Quater","Entity_Name","Amount","Count"))


mycursor.execute("SELECT * FROM top_user")
mydb.commit()
tab_6 = mycursor.fetchall()
Top_User = pd.DataFrame(tab_6, columns = ("State","Year","Quater","Name","Registered_Users"))


def A_Year(df, year):
    aty = df[df["Year"]==year]
    aty.reset_index(drop=True,inplace = True)

    atyg = aty.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    atyg.reset_index(inplace = True)
    
    T_count = px.bar(atyg,x="State",y="Transaction_count",title=f"{year} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Sunset,height = 550, width = 800)
    st.plotly_chart(T_count)

    T_amt = px.bar(atyg,x="State",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Oryel_r,height = 550, width = 800)
    st.plotly_chart(T_amt)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    State_names=[]
    for data in data1["features"]:
        State_names.append(data["properties"]["ST_NM"])

    fig_ind1 = px.choropleth(atyg,geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_count", color_continuous_scale= "Viridis_r",
                            range_color= (atyg["Transaction_count"].min(),atyg["Transaction_count"].max()),hover_name= "State",
                            title= f"{year} TRANSACTION COUNT",fitbounds= "locations", height = 650, width = 800)
    
    fig_ind1.update_geos(visible = False)
    st.plotly_chart(fig_ind1)
    

    fig_ind2 = px.choropleth(atyg,geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                            color= "Transaction_amount", color_continuous_scale= "Darkmint_r",
                            range_color= (atyg["Transaction_amount"].min(),atyg["Transaction_amount"].max()),hover_name= "State",
                            fitbounds= "locations", title= f"{year} TRANSACTION AMOUNT", height = 650, width = 800)
    
    fig_ind2.update_geos(visible = False)
    st.plotly_chart(fig_ind2)
    
    return aty


def A_quater(df,quater):
    auy = df[df["Quater"]==quater]
    auy.reset_index(drop=True,inplace = True)

    auyg = auy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    auyg.reset_index(inplace = True)

    T_count = px.bar(auyg,x="State",y="Transaction_count",title=f"{quater} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Magenta)
    st.plotly_chart(T_count)

    
    T_amt = px.bar(auyg,x="State",y="Transaction_amount",title=f"{quater} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.solar_r)
    st.plotly_chart(T_amt)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    State_names=[]
    for data in data1["features"]:
        State_names.append(data["properties"]["ST_NM"])

    fig_ind1 = px.choropleth(auyg,geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (auyg["Transaction_count"].min(),auyg["Transaction_count"].max()),hover_name= "State",
                                title= f"{quater} TRANSACTION COUNT",fitbounds= "locations", height = 650, width = 600,)
    
    fig_ind1.update_geos(visible = False)
    st.plotly_chart(fig_ind1)
        
    fig_ind2 = px.choropleth(auyg,geojson=data1, locations= "State", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (auyg["Transaction_amount"].min(),auyg["Transaction_amount"].max()),hover_name= "State",
                                title= f"{quater} TRANSACTION AMOUNT",fitbounds= "locations", height = 650, width = 600)
    
    fig_ind2.update_geos(visible = False)
    st.plotly_chart(fig_ind2)
    return auy       

def Aggre_transaction_plot(df, state):
        atr = df[df["State"]==state]
        atr.reset_index(drop=True,inplace = True)

        atrg = atr.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
        atrg.reset_index(inplace = True)

        col1, col2 = st.columns(2)

        with col1:
                T_count = px.bar(atrg,x="State",y="Transaction_count",title=f"{state.upper()} TRANSACTION COUNT",
                                 width = 600, height= 600,color_discrete_sequence=px.colors.sequential.Jet)
                st.plotly_chart(T_count)

        with col2:
                T_amt = px.bar(atrg,x="State",y="Transaction_amount",title=f"{state.upper()} TRANSACTION AMOUNT",
                               width = 600, height= 600,color_discrete_sequence=px.colors.sequential.ice_r)
                st.plotly_chart(T_amt)

def Aggre_user_plot(df, year):
        aus = df[df["Year"]==year]
        aus.reset_index(drop=True,inplace = True)

        ausg = aus.groupby("Year")[["count","percentage"]].sum()
        ausg.reset_index(inplace = True)

        T_count = px.bar(ausg,x="Year",y="count",title=f"{year} USER COUNT",
                            width = 1000,color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(T_count)

        
        T_amt = px.bar(ausg,x="Year",y="percentage",title=f"{year} USERS PERCENTAGE",
                        width = 1000,color_discrete_sequence=px.colors.sequential.Oranges_r)
        st.plotly_chart(T_amt)
        return aus

def Aggre_user_q_plot(df, quater):
        auq = df[df["Quater"]==quater]
        auq.reset_index(drop=True,inplace = True)

        auqg = auq.groupby("brand")[["count","percentage"]].sum()
        auqg.reset_index(inplace = True)

        U_count = px.pie(auqg,names="brand",values="count",title=f"QUATER {quater} USER COUNT BY BRAND",
                        hover_data= "percentage",width = 600, height= 600,color_discrete_sequence=px.colors.sequential.tempo_r)
        st.plotly_chart(U_count)

def Map_transaction_plot(df, year):
    mtr = df[df["Year"] == year]
    mtr.reset_index(drop=True, inplace=True)

    mtrg = mtr.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    mtrg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(mtrg, x= "State", y= "Transaction_count",
                              width=600, height=500, title= f"{year} MAP TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_2= px.bar(mtrg, x= "State", y= "Transaction_amount",
                              width=600, height= 500, title= f"{year} MAP TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
    
        st.plotly_chart(fig_map_bar_2)
    return mtr

def Map_transaction_plot_2(df, quater):
    mtr = df[df["Quater"] == quater]
    mtr.reset_index(drop=True, inplace=True)

    mtrg = mtr.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    mtrg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(mtrg, x= "State", y= "Transaction_count",
                              width=600, height=500, title= f"QUATER {quater} MAP TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Inferno_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_2= px.bar(mtrg, x= "State", y= "Transaction_amount",
                              width=600, height= 500, title= f"QUATER {quater} MAP TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.YlOrRd_r)
    
        st.plotly_chart(fig_map_bar_2)
    return mtr

def Map_user_plot(df, state):
        mus = df[df["State"]==state]
        mus.reset_index(drop=True,inplace = True)

        musg = mus.groupby("State")[["Appopens","Registered_Users"]].sum()
        musg.reset_index(inplace = True)

        col1, col2 = st.columns(2)

        with col1:
                U_count = px.pie(musg,names="State",values="Appopens",title=f"{state.upper()} APPOPENS COUNT",
                                 width = 600, height= 600)
                st.plotly_chart(U_count)

        with col2:
                U_amt = px.pie(musg,names="State",values="Registered_Users",title=f"{state.upper()} REGISTERED USERS",
                               width = 600, height= 600)
                st.plotly_chart(U_amt)
        return mus

def Map_user_plot_1(df, districts):
        mus = df[df["Districts"]==districts]
        mus.reset_index(drop=True,inplace = True)

        musg = mus.groupby("Districts")[["Appopens","Registered_Users"]].sum()
        musg.reset_index(inplace = True)

        col1, col2 = st.columns(2)

        with col1:
                U_count = px.bar(musg,x="Districts",y="Appopens",title=f"{districts.upper()} APPOPENS COUNT",
                                 width = 600, height= 500,color_discrete_sequence=px.colors.sequential.deep_r)
                st.plotly_chart(U_count)

        with col2:
                U_users = px.bar(musg,x="Districts",y="Registered_Users",title=f"{districts.upper()} REGISTERED USERS",
                               width = 600, height= 500,color_discrete_sequence=px.colors.sequential.Cividis)
                st.plotly_chart(U_users)
        return mus

def Top_transaction_plot(df, state):
        ttr = df[df["State"]==state]
        ttr.reset_index(drop=True,inplace = True)

        ttrg = ttr.groupby("Entity_Name")[["Amount","Count"]].sum()
        ttrg.reset_index(inplace = True)
                
        col1, col2 = st.columns(2)

        with col1:
                T_count = px.bar(ttrg,x="Entity_Name",y="Amount",title=f"{state.upper()} TRANSACTION AMOUNT",
                                 width = 600, height= 600,color_discrete_sequence=px.colors.sequential.Viridis)
                st.plotly_chart(T_count)

        with col2:
                T_amt = px.bar(ttrg,x="Entity_Name",y="Count",title=f"{state.upper()} TRANSACTION COUNT",
                               width = 600, height= 600,color_discrete_sequence=px.colors.sequential.Bluered_r)
                st.plotly_chart(T_amt)
        return ttr

def Top_user_plot(df, state):
    tur = df[df["State"] == state]
    tur.reset_index(drop=True, inplace=True)

    turg = tur.groupby("State")[["Registered_Users"]].sum()
    turg.reset_index(inplace=True)


    T_amt = px.bar(turg,x="State",y="Registered_Users",title=f"{state.upper()} REGISTERED USERS",
                    width = 600, height= 600,color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(T_amt)

# QUESTIONS

def question1():
    q1 = Agg_Trans[["State","Transaction_count"]]
    q1a = q1.groupby("State")["Transaction_count"].sum().sort_values(ascending = False)
    q1b = pd.DataFrame(q1a).head(10).reset_index()

    ans = px.pie(q1b,names="State",values="Transaction_count",title="TOP 10 STATES TRANSACTION COUNT",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Cividis_r)
    return st.plotly_chart(ans)

def question2():
    q2 = Agg_Trans[["State","Transaction_amount"]]
    q2a = q2.groupby("State")["Transaction_amount"].sum().sort_values(ascending = False)
    q2b = pd.DataFrame(q2a).head(20).reset_index()

    ans = px.pie(q2b,names="State",values="Transaction_amount",title="TOP 20 STATES TRANSACTION AMOUNT",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.solar)
    return st.plotly_chart(ans)

def question3():
    q3 = Agg_User[["brand","count"]]
    q3a = q3.groupby("brand")["count"].sum().sort_values(ascending = False)
    q3b = pd.DataFrame(q3a).head(10).reset_index()

    ans = px.bar(q3b,x="count",y="brand",orientation='h',title="TOP 10 BRANDS USER COUNT",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(ans)

def question4():
    q4 = Agg_User[["State","count"]]
    q4a = q4.groupby("State")["count"].sum().sort_values(ascending = False)
    q4b = pd.DataFrame(q4a).head(20).reset_index()
    
    ans = px.bar(q4b,x="State",y="count",title="TOP 20 STATES USERS COUNT",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Viridis_r)
    return st.plotly_chart(ans)

def question5():
    q5 = Map_Trans[["Quater","Transaction_count"]]
    q5a = q5.groupby("Quater")["Transaction_count"].sum().sort_values(ascending = False)
    q5b = pd.DataFrame(q5a).head(20).reset_index()
    
    ans = px.bar(q5b,x="Quater",y="Transaction_count",title="TRANSACTION COUNT OF 4 QUATERS ",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Darkmint_r)
    return st.plotly_chart(ans)

def question6():
    q6 = Map_User[["Districts","Registered_Users"]]
    q6a = q6.groupby("Districts")["Registered_Users"].sum().sort_values(ascending = False)
    q6b = pd.DataFrame(q6a).head(20).reset_index()
    
    ans = px.bar(q6b,x="Registered_Users",y="Districts",orientation='h',title="TOP 20 DISTRICTS REGISTERED USERS COUNT",
                width = 700, height= 600, color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    return st.plotly_chart(ans)

def question7():
    q7 = Top_Trans[["State","Entity_Name"]]
    q7a = q7.groupby("State")["Entity_Name"].nunique().sort_values(ascending = False)
    q7b = pd.DataFrame(q7a).head(20).reset_index()
    
    ans = px.pie(q7b,names="State",values="Entity_Name",title="TOP 20 ENTITY COUNT BY STATEWISE ",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    return st.plotly_chart(ans)

def question8():
    q8 = Agg_User[["State","count"]]
    q8a = q8.groupby("State")["count"].sum().sort_values(ascending = True)
    q8b = pd.DataFrame(q8a).head(10).reset_index()
    
    ans = px.bar(q8b,x="State",y="count",title="LOWEST 10 STATES USERS COUNT",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Oryel_r)
    return st.plotly_chart(ans)

def question9():
    q9 = Agg_Trans[["State","Transaction_count"]]
    q9a = q9.groupby("State")["Transaction_count"].sum().sort_values(ascending = True)
    q9b = pd.DataFrame(q9a).head(10).reset_index()

    ans = px.pie(q9b,names="State",values="Transaction_count",title="10 LOWEST TRANSACTION COUNT STATES",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Jet_r)
    return st.plotly_chart(ans)

def question10():
    q10 = Agg_User[["brand","count"]]
    q10a = q10.groupby("brand")["count"].sum().sort_values(ascending = True)
    q10b = pd.DataFrame(q10a).head(10).reset_index()

    ans = px.bar(q10b,x="count",y="brand",orientation='h',title="LOWEST 10 USERS COUNT BRANDS",
                width = 600, height= 600, color_discrete_sequence=px.colors.sequential.Mint_r)
    return st.plotly_chart(ans)

# Stremlit
st.set_page_config(layout= "wide")
st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]")
select = st.sidebar.radio("Main Menu",["HOME","DATA","TOP CHARTS"])

if select == "HOME":
    
    st.header(':rainbow[USED SKILLS:]')
    st.write(' :star: Github Cloning') 
    st.write(' :star: Python')
    st.write(' :star: Pandas')
    st.write(' :star: MySQL')
    st.write(' :star: mysql-connector-python')
    st.write(' :star: Streamlit')
    st.write(' :star: Plotly')

    st.header(':rainbow[PROJECT SUMMARY:]')
    st.subheader('Data extraction:')
    st.write("""Clone the Github using scripting to fetch the data from the
                Phonepe pulse Github repository and store it in a suitable format such as CSV
                or JSON""")
    st.subheader('Data transformation:')
    st.write("""Used a scripting language such as Python, along with
                libraries such as Pandas, to manipulate and pre-process the data. This may
                include cleaning the data, handling missing values, and transforming the data
                into a format suitable for analysis and visualization""")
    st.subheader('Data insertion:')
    st.write("""Used the "mysql-connector-python" library in Python to
                connect to a MySQL database and insert the transformed data using SQL
                commands""")
    st.subheader('Dashboard creation:')
    st.write("""Used the Streamlit and Plotly libraries in Python to create
                an interactive and visually appealing dashboard. Plotly's built-in geo map
                functions can be used to display the data on a map and Streamlit can be used
                to create a user-friendly interface with multiple dropdown options for users to
                select different facts and figures to display""")
    st.subheader('Data retrieval:')
    st.write("""Used the "mysql-connector-python" library to connect to the
                MySQL database and fetch the data into a Pandas dataframe. Use the data in
                the dataframe to update the dashboard dynamically""")


elif select == "DATA":
     
     tab1,tab2,tab3 = st.tabs(["Aggregated_Analysis","Map_Analysis","Top_Analysis"])

     with tab1:
          method = st.radio("Select the option",["Transaction_Analysis","User_Analyis"])
          
          if method == "Transaction_Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Agg_Trans["Year"].min(),Agg_Trans["Year"].max())
            vis_agg_trns_y = A_Year(Agg_Trans, years)
            
            col1,col2 = st.columns(2)
            with col1:
                 quaters = st.slider("Select the quater",vis_agg_trns_y["Quater"].min(),vis_agg_trns_y["Quater"].max())
            vis_agg_trns_q = A_quater(vis_agg_trns_y, quaters)
                 
            state_y_q= st.selectbox("Select the State",vis_agg_trns_q["State"].unique())

            Aggre_transaction_plot(vis_agg_trns_q,state_y_q)

          elif method == "User_Analyis":
               
               col1,col2 = st.columns(2)
               with col1:
                    Years_1 = st.selectbox("Select the Year",Agg_User["Year"].unique())
               vis_agg_user_y = Aggre_user_plot(Agg_User, Years_1)
               
               col1,col2 = st.columns(2) 
               with col1:
                    quaters_1 = st.selectbox("Select the Quater",vis_agg_user_y["Quater"].unique())
               vis_agg_user_s = Aggre_user_q_plot(vis_agg_user_y, quaters_1)
             
     with tab2:
          method_2 = st.radio("Select the Option",["Map_Transaction_Analysis","Map_User_Analyis"])

          if method_2 == "Map_Transaction_Analysis":
               col1,col2 = st.columns(2)
               with col1:
                    years_2 = st.slider("Select the Map Year",Map_Trans["Year"].min(),Map_Trans["Year"].max())
               vis_map_trns_y = Map_transaction_plot(Map_Trans, years_2)
                
               col1,col2 = st.columns(2)
               with col1:
                   quaters_2 = st.slider("Select the Map quater",vis_map_trns_y["Quater"].min(),vis_map_trns_y["Quater"].max())
               vis_map_trns_q = Map_transaction_plot_2(vis_map_trns_y, quaters_2)

          if method_2 == "Map_User_Analyis":
               col1,col2 = st.columns(2)
               with col1:
                    state = st.selectbox("Select the state",Map_User["State"].unique())
               vis_map_user_s = Map_user_plot(Map_User, state)
                
               col1,col2 = st.columns(2)
               with col1:
                    districts = st.selectbox("Select the Districts",vis_map_user_s["Districts"].unique())
               vis_map_user_d = Map_user_plot_1(vis_map_user_s, districts)
          
     with tab3:
          method_3 = st.radio("Select Option",["Top_Transaction_Analysis","Top_User_Analyis"])

          if method_3 == "Top_Transaction_Analysis":
               
               col1,col2 = st.columns(2)
               with col1:
                    State = st.selectbox("Select the State",Top_Trans["State"].unique())
               vis_top_trans_s = Top_transaction_plot(Top_Trans, State)
                
          if method_3 == "Top_User_Analyis":  
               
               col1,col2 = st.columns(2)
               with col1:
                    State = st.selectbox("Select State",Top_User["State"].unique())
               vis_top_user_s = Top_user_plot(Top_User, State)
     
elif select =="TOP CHARTS":
     ques = st.selectbox("Select the Question:",('Top 10 States Transaction Count','Top 20 States Transaction Amount',
                                                 'Top 10 Brands User Count','Top 20 States User Count','Transaction count of 4 Quaters',
                                                 'Top 20 District Registered User Count','Top 20 Entity Count by StateWise',
                                                 'Lowest 10 States Users Count','10 Lowest Transaction count states',
                                                 'Lowest 10 Users count brands'))
               
               
     if ques =='Top 10 States Transaction Count':
          question1()
    
     elif ques =='Top 20 States Transaction Amount':
          question2()

     elif ques =='Top 10 Brands User Count':
          question3()

     elif ques =='Top 20 States User Count':
          question4()

     elif ques =='Transaction count of 4 Quaters':
          question5()

     elif ques =='Top 20 District Registered User Count':
          question6()

     elif ques =='Top 20 Entity Count by StateWise':
          question7()

     elif ques =='Lowest 10 States Users Count':
          question8()

     elif ques =='10 Lowest Transaction count states':
          question9()

     elif ques =='Lowest 10 Users count brands':
          question10()
     


    




