#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess
import sqlalchemy
import pymysql
import mysql
import mysql.connector
from matplotlib import pyplot as plt
from mysql.connector import connection
import plotly.express as px
import pandas as pd
import requests
from PIL import Image
from sqlalchemy import create_engine
import plotly.graph_objects as go
from git.repo.base import Repo
from sqlalchemy.dialects import mysql
import plotly.io as pio
from pathlib import Path
import base64
import streamlit as st
import seaborn as sns


# In[2]:


profile = Image.open(r"C:\Users\user\Desktop\PhonePe_Logo-2048x2042.png")

st.set_page_config(page_title='PhonePe Pulse', page_icon=profile, layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)


# In[3]:


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{r"https://bfsi.eletsonline.com/wp-content/uploads/2021/10/PhonePe-Pulse.jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


st.title(':blue[PhonePe Pulse Analysis Dashboard]')


# In[4]:


page_element = """
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://wallpapercave.com/wp/wp9274695.jpg");
  background-size: cover;
}

[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
<script>
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://mcdn.wallpapersafari.com/medium/89/87/X7GDE5.jpg");
background-size: cover;
}
</script>
"""

st.markdown(page_element, unsafe_allow_html=True)


# In[5]:


path_to_json1 = r"C:\Users\user\Desktop\Extract\data\aggregated\transaction\country\india\state"
aggregate_state_list = os.listdir(path_to_json1)

column1 = {'State': [], 'Year': [], 'Quater': [], 'Transaction_type': [], 'Transaction_count': [],
           'Transaction_amount': []
           }

for i in aggregate_state_list:
    path_i = os.path.join(path_to_json1, i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i, j)
        aggregate_year_list = os.listdir(path_j)

        for k in aggregate_year_list:
            path_k = os.path.join(path_j, k)
            json_data = open(path_k, 'r')
            dict1 = json.load(json_data)

            for m in dict1['data']['transactionData']:
                name = m['name']
                count = m['paymentInstruments'][0]['count']
                amount = m['paymentInstruments'][0]['amount']
                column1['Transaction_type'].append(name)
                column1['Transaction_count'].append(count)
                column1['Transaction_amount'].append(amount)
                column1['State'].append(i)
                column1['Year'].append(j)
                column1['Quater'].append(int(k.strip('.json')))

aggregated_transaction_DF = pd.DataFrame(column1)


# In[6]:


path_to_json2 = r"C:\Users\user\Desktop\state"
users = os.listdir(path_to_json2)

column2 = {'State': [], 'Year': [], 'Quater': [], 'brands': [], 'Count': [], 'Percentage': []}

my_list = list()
for i in users:
    path_i = os.path.join(path_to_json2 , i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i , j)
        aggregate_year_list = os.listdir(path_j)

        for m in aggregate_year_list:
            path_m = os.path.join(path_j , m)
            json_data = open(path_m, 'r')
            dict2 = json.load(json_data)
            try:
                my_list = dict2['data']['usersByDevice'][:]
            except:
                pass

                # print(dict2['data']['usersByDevice'][:])
            try:
                for n in range(0, len(my_list)):
                    brand_name = my_list[n]['brand']
                    count = my_list[n]['count']
                    percentages = my_list[n]['percentage']
                    column2['brands'].append(brand_name)
                    column2['Count'].append(count)
                    column2['Percentage'].append(percentages)
                    column2['State'].append(i)
                    column2['Year'].append(j)
                    column2['Quater'].append(int(m.strip('.json')))
            except:
                pass

aggregated_users_DF = pd.DataFrame(column2)


# In[7]:


path_to_json3 = r"C:\Users\user\Desktop\Extract\data\map\transaction\hover\country\india\state"
map_hovering_list = os.listdir(path_to_json3)

column3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'count': [], 'amount': []}

for i in map_hovering_list:
    path_i = os.path.join(path_to_json3, i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i, j)
        aggregate_year_list = os.listdir(path_j)

        for m in aggregate_year_list:
            path_m = os.path.join(path_j, m)
            with open(path_m, 'r') as json_file:
                dict3 = json.load(json_file)

            for n in dict3['data']['hoverDataList']:
                district = n['name']
                count = n['metric'][0]['count']
                amount = n['metric'][0]['amount']
                column3['District'].append(district)
                column3['count'].append(count)
                column3['State'].append(i)
                column3['Year'].append(j)
                column3['amount'].append(amount)
                column3['Quarter'].append(int(m.strip('.json')))

map_transactions_DF = pd.DataFrame(column3)


# In[8]:


path_to_json4 = r"C:\Users\user\Desktop\Extract\data\map\user\hover\country\india\state"
list_maps = os.listdir(path_to_json4)

column4 = {'State': [], 'Year': [], 'Quater': [], 'District': [], 'RegisteredUser': []}

for i in list_maps:
    path_i = os.path.join(path_to_json4,i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i,j)
        aggregate_year_list = os.listdir(path_j)

        for m in aggregate_year_list:
            path_m = os.path.join(path_j,m)
            with open(path_m, 'r') as json_file:
                dict4 = json.load(json_file)

            for n in dict4['data']['hoverData'].items():
                district = n[0]
                registeredUser = n[1]['registeredUsers']
                column4['District'].append(district)
                column4['RegisteredUser'].append(registeredUser)
                column4['State'].append(i)
                column4['Year'].append(j)
                column4['Quater'].append(int(m.strip('.json')))

users_map_DF = pd.DataFrame(column4)


# In[9]:


path_to_json5 = r"C:\Users\user\Desktop\Extract\data\top\transaction\country\india\state"
list_of_tops = os.listdir(path_to_json5)

column5 = {'State': [], 'Year': [], 'Quater': [], 'District': [], 'Transaction_count': [],
           'Transaction_amount': []
           }
for i in list_of_tops:
    path_i = os.path.join(path_to_json5 , i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i , j)
        aggregate_year_list = os.listdir(path_j)

        for m in aggregate_year_list:
            path_m = os.path.join(path_j , m)
            with open(path_m, 'r') as json_file:
                dict5 = json.load(json_file)

            for n in dict5['data']['pincodes']:
                name = n['entityName']
                count = n['metric']['count']
                amount = n['metric']['amount']
                column5['District'].append(name)
                column5['Transaction_count'].append(count)
                column5['Transaction_amount'].append(amount)
                column5['State'].append(i)
                column5['Year'].append(j)
                column5['Quater'].append(int(m.strip('.json')))

top_user_transactions_DF = pd.DataFrame(column5)


# In[10]:


path_to_json6 = r"C:\Users\user\Desktop\Extract\data\top\user\country\india\state"
list_of_users = os.listdir(path_to_json6)

column6 = {'State': [], 'Year': [], 'Quater': [], 'District': [], 'RegisteredUser': []}

for i in list_of_users:
    path_i = os.path.join(path_to_json6 , i)
    aggregate_year = os.listdir(path_i)

    for j in aggregate_year:
        path_j = os.path.join(path_i , j)
        aggregate_year_list = os.listdir(path_j)

        for m in aggregate_year_list:
            path_m = os.path.join(path_j , m)
            with open(path_m, 'r') as json_file:
                dict6 = json.load(json_file)

            for n in dict6['data']['pincodes']:
                name = n['name']
                registeredUser = n['registeredUsers']
                column6['District'].append(district)
                column6['RegisteredUser'].append(registeredUser)
                column6['State'].append(i)
                column6['Year'].append(j)
                column6['Quater'].append(int(m.strip('.json')))

top_users_DF = pd.DataFrame(column6)


# In[11]:


aggregated_users_DF.to_csv('aggregated_users_DF.csv',index=False)
map_transactions_DF.to_csv('map_transactions_DF.csv',index=False)
users_map_DF.to_csv('users_map_DF.csv',index=False)
top_user_transactions_DF.to_csv('top_user_transactions_DF.csv',index=False)
top_users_DF.to_csv('top_users_DF.csv',index=False)
aggregated_transaction_DF.to_csv('aggregated_transaction_DF.csv',index=False)


# In[12]:


import pandas as pd

# Load the individual CSV files into DataFrames
aggregated_users_DF = pd.read_csv('aggregated_users_DF.csv')
map_transactions_DF = pd.read_csv('map_transactions_DF.csv')
users_map_DF = pd.read_csv('users_map_DF.csv')
top_user_transactions_DF = pd.read_csv('top_user_transactions_DF.csv')
top_users_DF = pd.read_csv('top_users_DF.csv')
aggregated_transaction_DF = pd.read_csv('aggregated_transaction_DF.csv')
longitude_latitude_DF = pd.read_csv(r"C:\Users\user\Desktop\New folder\Data_Map_Districts_Longitude_Latitude.csv")
# Combine the DataFrames into a single DataFrame
consolidated_df = pd.concat([
    aggregated_users_DF,
    map_transactions_DF,
    users_map_DF,
    top_user_transactions_DF,
    top_users_DF,
    aggregated_transaction_DF,
    longitude_latitude_DF
], ignore_index=True)

# Save the consolidated DataFrame to a CSV file
consolidated_df.to_csv('consolidated_data.csv', index=False)


# In[13]:


consolidated_df = pd.read_csv("consolidated_data.csv")
consolidated_df['State'] = consolidated_df['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana',
'tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})
consolidated_df['Transaction_type'].replace('Peer-to-peer payments', 'Peer_to_peer payments', inplace=True)

df = consolidated_df

import pandas as pd

columns_to_remove = ['brands', 'Count', 'Percentage', 'Percentage', 'count','amount','Quater','RegisteredUser']

consolidated_df = df.drop(columns=columns_to_remove)


table_select_dict = {"Aggregate of Transactions": 'aggregated_transaction_tbl',
                     "Aggregated Info of Registered Users": "aggregated_users_tbl",
                     "Transactions Geography": "map_transactions_tbl",
                     "RegisterUsers Information as of Geography": "users_map_tbl",
                     "Top Transactions": "top_user_transactions_tbl",
                     "Top RegisteredUsers": "top_users_tbl"}

select_items = st.selectbox('***Select***', ["Aggregate of Transactions",
                                             "Aggregated Info of Registered Users",
                                             "RegisterUsers Information as of Geography",
                                             "Top Transactions", "Top RegisteredUsers"]
                            )

st.write(f"You have selected : {select_items}")
Year = st.selectbox("Select an Year", ('2018', '2019', '2020', '2021', '2022'))

Quarter = st.selectbox("Select The Quarter", ('1', '2', '3', '4'))
st.write(f"You have selected {Quarter} Quarter")

filter_by = st.selectbox("***Select***",
                         ['Transaction_count',
                          'Transaction_amount',
                          'RegisteredUsers',
                          'count',
                          'brands',
                          'Percentage',
                          'amount',
                          'brands',
                          'Count'])

st.write(f"You have selected the filter {filter_by}")

sql = f'select * from {table_select_dict[select_items]} where year={Year} and Quater={Quarter}'

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/phonepe_pulse", pool_size=1000,
                       max_overflow=2000)

mysql_df = pd.read_sql_query(sql, engine)

for column in mysql_df:
    if mysql_df[column].dtype == 'float64':
        mysql_df[column] = pd.to_numeric(mysql_df[column], downcast='float')
        if mysql_df[column].dtype == 'int64':
            mysql_df[column] = mysql_df.to_numeric(mysql_df[column], downcast='integer')
st.write(mysql_df)

def scatterplot(mysql_df):
    if filter_by == 'Transaction_type':
        fin_filter_val = 'Transaction_amount'
        if filter_by == "amount":
            fin_filter_val = 'amount'
            data = [dict(
                type='scatter',
                x=mysql_df['State'],
                y=mysql_df[fin_filter_val],
                mode='markers',
                transforms=[dict(
                    type='groupby',
                    groups=mysql_df['State'],
                )]
            )]

            fig_dict = dict(data=data)
            pio.show(fig_dict, validate=False)
            st.plotly_chart(fig_dict)

            fig_1 = px.line(mysql_df, x='State', y=fin_filter_val)
            fig_1.show()

    scatterplot(mysql_df)


col1, col2 = st.columns(2)

import mysql.connector

connection = mysql.connector.connect(user="root", password="12345", database="phonepe_pulse")
cursor = connection.cursor()

with col1:
    st.subheader(':blue[Phonepe Transaction Data Visualization]')
    States = aggregated_transaction_DF['State'].unique()
    options = st.selectbox("****select options****", States)
    options_df = aggregated_transaction_DF[aggregated_transaction_DF['State'] == options]
    figure1 = px.bar(options_df, x="Transaction_type", y="Transaction_count", color="Transaction_type",
                     title='Phonepe Transaction data Visualization')
    st.plotly_chart(figure1, use_container_width=True)

with col2:
    st.subheader("Data Analysis Transaction Count as per Year/Quarter")
    data_by_year_quater = consolidated_df.groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
    figure2 = px.bar(data_by_year_quater, y='Transaction_count', x='Year', color='Quarter',
                     title='Data Analysis Transaction Count as per Year/Quarter')
    st.plotly_chart(figure2, use_container_width=True)


# In[14]:


st.subheader(':blue[OVERALL BRAND ANALYSIS]')
for column in aggregated_users_DF:
    if aggregated_users_DF[column].dtype == 'float64':
        aggregated_users_DF[column] = pd.to_numeric(aggregated_users_DF[column], downcast='float')
        if aggregated_users_DF[column].dtype == 'int64':
            aggregated_users_DF[column] = aggregated_users_DF.to_numeric(aggregated_users_DF[column],
                                                                         downcast='integer')

fig8 = px.pie(aggregated_users_DF, values="Percentage", names="brands", title="Percentage Share of All Mobile Brands")
fig8.update_traces(textposition='inside', textinfo='percent+label')
fig8.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font_color': '#333',
    'hoverlabel': {
        'font': {'color': '#fff'},
        'bgcolor': 'royalblue'
    }
})
st.plotly_chart(fig8, use_container_width=True)
st.info(""" Observation:
            User can observe percentage share of each brand for phonepe transaction""")

csv_path = r"C:\Users\user\Desktop\New folder\Data_Map_IndiaStates_TU.csv"
india = pd.read_csv(csv_path)
year = st.selectbox("Please select the year", ('2018', '2019', '2020', '2021', '2022'), key="k9")
agg_trans = aggregated_transaction_DF["State"].drop_duplicates().sort_values()
agg_trans_DF = pd.DataFrame(agg_trans)
group_by_state = aggregated_transaction_DF.groupby("State", sort=True).sum()
merged_df = pd.merge(aggregated_users_DF, group_by_state, on="State")
total_df = pd.merge(group_by_state, merged_df, on="State")
total_df1 = total_df[total_df['Year'] == year]

st.write(":blue[line chart to show overall growth of phonepe in last 5 years]")

a = aggregated_transaction_DF.groupby("Year").sum()
b = aggregated_transaction_DF['Year'].drop_duplicates().sort_values()
years = pd.DataFrame(b)
c = pd.merge(years, a, on="Year")

fig_year = px.line(
    c,
    x="Year",
    y="Transaction_count"
)

fig_year.update_layout(
    title='Total Transactions by Year',
    xaxis_title='Year',
    yaxis_title='Total Transactions',

)

fig_year.update_traces(
    line=dict(color='blue', width=2),
    mode='lines+markers',
    marker=dict(size=5, color='red', symbol='circle'),
    fill='tozeroy',
    fillcolor='rgba(0,176,246,0.2)'
)
st.plotly_chart(fig_year, use_container_width=True)


# In[15]:


merged_by_states_Trans_count = merged_df.sort_values(by='Transaction_count')

fig_trans_bar = px.bar(merged_by_states_Trans_count,
                       x="State",
                       y='Transaction_count',
                       color="State",
                       color_discrete_sequence=px.colors.qualitative.Pastel,
                       title='Total Transactions By State')
fig_trans_bar.update_layout(xaxis_title='State', yaxis_title="Total Transactions", font=dict(family="Arial", size=14))
with st.expander("SEE BAR GRAPH FOR THE STATES"):
    st.plotly_chart(fig_trans_bar, use_container_width=True)
    st.info(
        ":blue[the above bar graph shows the transaction done in each states in increasing order. Here you can observe the top states having higher transaction]")

Data_Aggregated_Transaction_df = pd.read_csv(
    r"C:\Users\user\Desktop\New folder\Data_Aggregated_Transaction_Table.csv")
Data_Aggregated_User_Summary_df = pd.read_csv(
    r"C:\Users\user\Desktop\New folder\Data_Aggregated_User_Summary_Table.csv")
Data_Aggregated_User_df = pd.read_csv(r"C:\Users\user\Desktop\New folder\Data_Aggregated_User_Table.csv")
Scatter_Geo_Dataset = pd.read_csv(
    r"C:\Users\user\Desktop\New folder\Data_Map_Districts_Longitude_Latitude.csv")
Choropleth_Dataset = pd.read_csv(r"C:\Users\user\Desktop\New folder\Data_Map_IndiaStates_TU.csv")
Data_Map_Transaction_df = pd.read_csv(r"C:\Users\user\Desktop\New folder\Data_Map_Transaction_Table.csv")
Data_Map_User_Table = pd.read_csv(r"C:\Users\user\Desktop\New folder\Data_Map_User_Table.csv")
Indian_States = pd.read_csv(r"C:\Users\user\Desktop\New folder\Longitude_Latitude_State_Table.csv")
colT1, colT2 = st.columns([2, 8])
with colT2:
    st.title(':blue[PhonePe Pulse Data Analysis:signal_strength:]')

# BAR CHART - TOP PAYMENT TYPE
import mysql.connector

connection = mysql.connector.connect(user="root", password="12345", database="phonepe_pulse")
mycursor = connection.cursor()

Selected_Year = st.selectbox("Select an Year", options=('2018', '2019', '2020', '2021', '2022'), key='kY')
Selected_Quarter = st.selectbox("Select The Quarter", options=('1', '2', '3', '4'), key='Kq')

mycursor.execute(
    f"select Transaction_type, sum(Transaction_count) as Total_Transactions, "
    f"round(sum(Transaction_amount), 7) as Total_amount "
    f"from aggregated_transaction_tbl "
    f"where Year= {Selected_Year} and Quater = {Selected_Quarter} "
    f"group by Transaction_type order by Transaction_type")
df = pd.DataFrame(mycursor.fetchall(),
                  columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])
fig = px.bar(df,
             title='Transaction Types vs Total_Transactions',
             x="Transaction_type",
             y="Total_Transactions",
             orientation='v',
             color='Total_amount',
             color_continuous_scale=px.colors.sequential.Agsunset)
st.plotly_chart(fig, use_container_width=False)


# In[16]:


c1, c2 = st.columns(2)
with c1:
    Year = st.selectbox(
        'Please select the Year',
        ('2018', '2019', '2020', '2021', '2022'))
with c2:
    Quarter = st.selectbox(
        'Please select the Quarter',
        ('1', '2', '3', '4'))
year = int(Year)
quarter = int(Quarter)
Transaction_scatter_districts = Data_Map_Transaction_df.loc[
    (Data_Map_Transaction_df['Year'] == year) & (Data_Map_Transaction_df['Quarter'] == quarter)].copy()
Transaction_Choropleth_States = Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
Transaction_scatter_districts.drop(
    Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],
    axis=0, inplace=True)
# Dynamic Scatter geo Data Generation
Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'],
                                                                          ascending=False)
Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False)
Total_Amount = []
for i in Transaction_scatter_districts['Total_Amount']:
    Total_Amount.append(i)
Scatter_Geo_Dataset['Total_Amount'] = Total_Amount
Total_Transaction = []
for i in Transaction_scatter_districts['Total_Transactions_count']:
    Total_Transaction.append(i)
Scatter_Geo_Dataset['Total_Transactions'] = Total_Transaction
Scatter_Geo_Dataset['Year_Quarter'] = str(year) + '-Q' + str(quarter)
# Dynamic Choropleth
Choropleth_Dataset = Choropleth_Dataset.sort_values(by=['state'], ascending=False)
Transaction_Choropleth_States = Transaction_Choropleth_States.sort_values(by=['Place_Name'], ascending=False)
Total_Amount = []
for i in Transaction_Choropleth_States['Total_Amount']:
    Total_Amount.append(i)
Choropleth_Dataset['Total_Amount'] = Total_Amount
Total_Transaction = []
for i in Transaction_Choropleth_States['Total_Transactions_count']:
    Total_Transaction.append(i)
Choropleth_Dataset['Total_Transactions'] = Total_Transaction


# In[17]:


Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
Indian_States['Registered_Users'] = Choropleth_Dataset['Registered_Users']
Indian_States['Total_Amount'] = Choropleth_Dataset['Total_Amount']
Indian_States['Total_Transactions'] = Choropleth_Dataset['Total_Transactions']
Indian_States['Year_Quarter'] = str(year) + '-Q' + str(quarter)
fig = px.scatter_geo(Indian_States,
                     lon=Indian_States['Longitude'],
                     lat=Indian_States['Latitude'],
                     text=Indian_States['code'],
                     hover_name="state",
                     hover_data=['Total_Amount', "Total_Transactions", "Year_Quarter"],
                     )
fig.update_traces(marker=dict(color="pink", size=0.3))
fig.update_geos(fitbounds="locations", visible=False, )
# scatter plotting districts
Scatter_Geo_Dataset['col'] = Scatter_Geo_Dataset['Total_Transactions']
fig1 = px.scatter_geo(Scatter_Geo_Dataset,
                      lon=Scatter_Geo_Dataset['Longitude'],
                      lat=Scatter_Geo_Dataset['Latitude'],
                      color=Scatter_Geo_Dataset['col'],
                      size=Scatter_Geo_Dataset['Total_Transactions'],
                      hover_name="District",
                      hover_data=["State", "Total_Amount", "Total_Transactions", "Year_Quarter"],
                      title='District',
                      size_max=22, )
fig1.update_traces(marker=dict(color="red", line_width=1))  # rebeccapurple
# coropleth mapping india
fig_ch = px.choropleth(
    Choropleth_Dataset,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color="Total_Transactions",
)
fig_ch.update_geos(fitbounds="locations", visible=False, )
# combining districts states and coropleth
fig_ch.add_trace(fig.data[0])
fig_ch.add_trace(fig1.data[0])
st.write("### **:yellow[PhonePe India Map]**")
colT1, colT2 = st.columns([6, 4])
with colT1:
    st.plotly_chart(fig_ch, use_container_width=True)
with colT2:
    st.info(
        """
    Analysis of Map:
    * Color Depth Of The State: Total Transactions.
    * Size of the Circles : Total Transactions District wise.
    * Larger Circles:  Top Transactions(higher transactions)
    * Hovering over the MAP : Total transactions, Total amount, names of the Districts as
      per the Latitude and Longitude taken.
    """
    )
    st.info(
            """
    Take Away:
    * User can observe Transactions of PhonePe in both statewide and District Wide.
    * Highest Transactions By Year and Quarter
    * District Wise Transactions
        """
    )


# In[ ]:




