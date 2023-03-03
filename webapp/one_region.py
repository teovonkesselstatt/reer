import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np

def run_app():

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv('data/REER_annual.csv')

    # Drop first columns
    df = df.iloc[:, 2:]

    # Set the country column as the index
    df.set_index('Country', inplace=True)

    # Get list of regions
    regions = df.Region.unique()

    option = st.selectbox(
    'Select a Region',
    regions,
    index = 6)


    # Slider para elegir años
    values = st.slider(
        'Select a range of years',
        1960, 2022, (1960, 2022))

    # Get a plot per region
    region = option

    st.markdown('### ' + region)

    df_temp = df[df['Region'] == region]
    df_temp = df_temp.drop('Region', axis = 1)

    #df_temp = df_temp.drop(['Suriname','Venezuela'])

    df_temp = df_temp.T
    df_temp.astype(np.float64)

    paises = list(df_temp.columns)

    options = st.multiselect(
    'Select Countries',
    paises, paises)


    # Select decade
    df_temp = df_temp.loc[str(values[0]):str(values[1])]

    fig1, ax1 = plt.subplots(figsize=(12, 4))


    df_temp.plot(y = options, \
            ax = ax1)

    st.pyplot(fig1)

