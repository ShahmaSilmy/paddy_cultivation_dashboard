import streamlit as st
import pandas as pd
import os

#For Title
st.title("Paddy Cultivation Dashboard - Sri Lanka (2020 - 2023)")

#Loading the Data
def load_data():
    df = pd.read_csv("paddy_2020_2023_cleaned.csv")
    return df

df = load_data()

#Basic Information
st.write("### Preview of the Dataset")
st.dataframe(df.head())

st.sidebar.title("Filter Data")
year = st.sidebar.selectbox("Select Year",sorted(df['Year'].unique()))
season = st.sidebar.selectbox("Select Season",sorted(df['Season'].unique()))

#For filtered view
filtered_df = df[
    (df["Year"] == year) &
    (df["Season"] == season)
]

st.write(f"### Data for - {season} {int( year)}")
st.dataframe(filtered_df)

import os

def load_data():
    path = "paddy_2020_2023_cleaned.csv"
    if not os.path.exists(path):
        st.error(f"File not found: {path}")
        return pd.DataFrame()  # return empty df
    df = pd.read_csv(path)
    return df

##plot 1

import plotly.express as px

#Grouping by district and sum of production
prod_by_district = df.groupby('District')['Production_MT'].sum().reset_index()

#sort by production for good visualisation
prod_by_district = prod_by_district.sort_values(by="Production_MT",ascending=False)

#Get the bar chart
fig1 = px.bar(
    data_frame=prod_by_district,
    x = "District",
    y = "Production_MT",
    title = "Total Paddy Production by District (2020-2023)",
    color = "Production_MT",
    color_continuous_scale = "ylgn"
)

#to display it in the streamlit application
st.plotly_chart(fig1, use_container_width=True)

##plot 2

# Ensure 'Yield_Average' is numeric
avg_yield_trend = df.groupby("Year")['Yield_Average'].mean().reset_index()

# Explicitly convert 'Year' to integer after grouping to remove decimal points
avg_yield_trend['Year'] = avg_yield_trend['Year'].astype(int)

#plot using the plotly library
fig2 = px.line(
    avg_yield_trend,
    x = 'Year',
    y = 'Yield_Average',
    markers= True,
    title= "National Average Paddy Yield Trend (2020-2023)",
    labels = {'Yield_Average': 'Average Yield', 'Year': 'Year'},
    line_shape = "linear"
)

fig2.update_traces(
    mode = 'lines+markers',
    line = dict(color = 'green',width = 3),
    marker=dict(size=8)
)
fig2.update_layout(
    hovermode='x unified',
    template= 'plotly_white',
    xaxis=dict(
        tickformat = "d"
    )
)
st.plotly_chart(fig2, use_container_width=True)

#plot 3 

seasonal_df = df[df["District"] != "SRI LANKA"]

prod_by_district = seasonal_df.groupby("District")["Production_MT"].sum().reset_index()

prod_by_district = prod_by_district.sort_values(by="Production_MT",ascending=False)

#creating the bar chart
fig3 = px.bar(
    prod_by_district,
    x = "District",
    y = "Production_MT",
    title = "Total Paddy Production by District Level (2020 - 2023)",
    color = "Production_MT",
    color_continuous_scale="twilight"
)

#To display in the streamlit app
st.plotly_chart(fig3, use_container_width=True)

#plot 4

st.subheader("Districts' Contribution to the Total Paddy Production")

#Exclude national row if present
district_df = df[df["District"] != "SRI LANKA"]

district_production = district_df.groupby("District")["Production_MT"].sum().reset_index()

#creating pie chart
fig4 = px.pie(
    district_production,
    names="District",
    values="Production_MT",
    title = "Total Paddy Production by District in % (2020-2023)"  
)

#show chart
st.plotly_chart(fig4, use_container_width=True)
