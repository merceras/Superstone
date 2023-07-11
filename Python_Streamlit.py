import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import datetime
import plotly.figure_factory as ff
from streamlit_multipage import MultiPage

st.set_page_config(page_title="Sample Superstone Dashboard", page_icon="bar_chart",layout="wide")
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

        
st.title("Sample Supersore Dashboard using Python")
f = st.file_uploader("Upload a file", type=(["csv","txt","xlsx","xls"]))
if f is not None:
    path_in = f.name
    st.write(path_in)
    df=pd.read_csv(path_in, lineterminator='\n',encoding = "ISO-8859-1" )
else:
     #os.chdir(r"C:\")
     df=pd.read_csv(r"Sample - Superstore.csv", lineterminator='\n',encoding = "ISO-8859-1" )

df["Order Date"] = pd.to_datetime(df["Order Date"])
startDate = pd.to_datetime(df['Order Date'].min())
endDate = pd.to_datetime(df['Order Date'].max())

#st.slider("Select Date",startDate.year,endDate.year)

col5, col6 = st.columns((2,2))

with col5:
    date1=pd.to_datetime(st.date_input("Start Date",startDate))
with col6:
   date2=pd.to_datetime(st.date_input("Start Date",endDate))
   df=df[(df["Order Date"]>=date1) & (df["Order Date"]<=date2)]

st.sidebar.header("Choose your filter :")

region=st.sidebar.multiselect('Pick the Region', df['Region'].unique())
if not region:
   df2 = df.copy()
else:
   df2= df[df['Region'].isin(region)]
state=st.sidebar.multiselect('Pick the State', df2['State'].unique())
if not state:
   df3 = df2.copy()
else:
    df3= df2[df2['State'].isin(state)]
city=st.sidebar.multiselect('Pick the City', df3['City'].unique())

if not region and not state and not city :
    filtered_df=df
elif not state and not city:
   filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df3['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
   filtered_df = df3[df3['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
   filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state)]
elif city:
   filtered_df = df3[df3['City'].isin(city)]
else:
  filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

#category_df=filtered_df.groupby("Category").sum()
category_df=filtered_df
#st.write(category_df)
with col5:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(y=category_df["Sales"], x=category_df["Category"],name="Category",text=category_df["Sales"],              
        marker=dict(
                color='#004953',
                line=dict(color='#004953', width=1)
        )))
        fig1.update_layout(
        width=150,
        height=400,
        plot_bgcolor='#ffe0c0',
        paper_bgcolor='#ffe0c0',  
        ) 
        fig1.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig1, use_container_width=True,height=200)
with col6:
        fig = px.pie(filtered_df,values="Sales",names="Region",title="Total Sales % as per Region",hole=.5)
        fig.update_traces(text=filtered_df["Region"],textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
fig2 = px.line(pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum()).reset_index(), 
x="month_year",
y="Sales", 
labels={"Sales": "Amount"},
title="Month_Wise Sales",height=500, width=1000,template="gridon")
st.plotly_chart(fig2, use_container_width=True)
with st.expander("View Data"):
        fig4 = go.Figure(data=[go.Table(
        header=dict(values=list(['Region','State','City','Category','Sales','Quantity']),
        line_color='darkslategray',
        fill_color='lightskyblue',
        align='left'),
        cells=dict(values=[df.Region,df.State,df.City,df.Category,df.Sales,df.Quantity], # 2nd column
        line_color='darkslategray',
        fill_color='lightcyan',
        align='left'))
        ])

        fig4.update_layout(width=800, height=700)
        st.plotly_chart(fig4,use_container_width=True)
        csv = filtered_df.to_csv().encode('utf-8')
        st.download_button('Dowload data',data=csv,file_name="Data.csv", mime='text/csv')



