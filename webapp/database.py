import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from sympy import subsets

@st.cache
def highlight_shock(number):
    if type(number) == int or type(number) == float:
        if number < -0.03:
            return 'color: red'
        elif number > 0.03:
            return 'color: green'
    else: return

def run_app():

    df = pd.read_csv("db.csv")
    df1 = df[df['year']>1999]
    st.dataframe(df1[['country','year','inflation','deviation','ToT','VarToT']].style.applymap(highlight_shock, subset = 'VarToT'))
