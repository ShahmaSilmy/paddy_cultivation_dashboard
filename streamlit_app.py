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

