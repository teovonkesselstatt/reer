import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns

# Define the function that creates plots
def coefplot(results, area):
    '''
    Takes in results of OLS model and returns a plot of
    the coefficients with 95% confidence intervals.

    Removes intercept, so if uncentered will return error.
    '''
    # Create dataframe of results summary
    coef_df = pd.DataFrame(results.summary().tables[1].data)

    # Add column names
    coef_df.columns = coef_df.iloc[0]

    # Drop the extra row with column labels
    coef_df = coef_df.drop(0)

    # Set index to variable names
    coef_df = coef_df.set_index(coef_df.columns[0])

    # Change datatype from object to float
    coef_df = coef_df.astype(float)

    # Get errors; (coef - lower bound of conf interval)
    errors = coef_df['coef'] - coef_df['[0.025']

    # Append errors column to dataframe
    coef_df['errors'] = errors

    # Sort values by index
    coef_df = coef_df.sort_index()

    ### Plot Coefficients ###

    # x-labels
    variables = list(coef_df.index.values)

    # Add variables column to dataframe
    coef_df['variables'] = variables

    # Set sns plot style back to 'poster'
    # This will make bars wide on plot
    sns.set_context("poster")

    # Define figure, axes, and plot
    fig, ax = plt.subplots(figsize=(12, 8))

    coef_df  = coef_df[(coef_df.index.str.contains(area))]

    # Error bars for 95% confidence interval
    # Can increase capsize to add whiskers
    coef_df.plot(x='variables', y='coef', kind='bar',
                    ax=ax, color='none', fontsize=16,
                    ecolor='steelblue',capsize=0,
                    yerr='errors', legend=False)

    # Set title & labels
    plt.title('Coefficients of Features of ' + area + ' w/ 95% Confidence Intervals',fontsize=20)
    ax.set_ylabel('Coefficients',fontsize=16)
    ax.set_xlabel('',fontsize=22)

    # Coefficients
    ax.scatter(x=np.arange(coef_df.shape[0]),
                marker='o', s=80,
                y=coef_df['coef'], color='steelblue')

    # Line to define zero on the y-axis
    ax.axhline(y=0, linestyle='--', color='red', linewidth=1)

    st.pyplot(fig)

    # return plt.show()

# Plots
def plotVar(start_year, end_year, area):

    # Me quedo con el area que pide
    df_temp = df[df['Area'] == area]
    # La decada que pide
    mask = (df_temp.index.year >= int(start_year)) & (df_temp.index.year <= int(end_year))
    df_temp = df_temp.loc[mask]

    # Group the data by country
    grouped = df_temp.groupby('Country')

    # Create a new figure and axes
    fig, ax = plt.subplots(figsize=(7,4))

    # Loop over the groups and plot each one
    for country, group in grouped:
        group.plot(y='REER', ax=ax, label=country)

    # Add a legend to the plot
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    return plt.show()


def run_app():
    # Read the CSV file into a pandas dataframe
    df = pd.read_csv('data/REER_annual.csv')

    # Drop first columns
    df = df.iloc[:, 2:]

    # Turn into long dataframe, keeping first columns
    df = pd.melt(df, id_vars = ['Country', 'Region'], value_vars=df.columns[2:], var_name='Year', value_name='REER')
    df.set_index('Year', inplace = True)
    df.index = pd.to_datetime(df.index)

    # Change Areas
    df['Area'] = df.loc[:, 'Region']
    df.loc[(df['Region'].str.contains('South America|Central America|Caribbean')), 'Area'] = 'Latin America'
    df.loc[(df['Region'].str.contains('Africa')), 'Area'] = 'Africa'
    df.loc[(df['Region'].str.contains('South-eastern Asia|Southern Asia')), 'Area'] = 'South Asia'
    df.loc[(df['Region'].str.contains('Western Asia|Central Asia')), 'Area'] = 'Middle East'
    df.loc[(df['Region'].str.contains('Southern Europe|Western Europe|Northern Europe')), 'Area'] = 'Western Europe'
    df.loc[(df['Region'].str.contains('Melanesia|Polynesia')), 'Area'] = 'Pacific Islands'
    df.loc[(df['Country'].str.contains('Russia')), 'Area'] = 'Russia'
    df.loc[(df['Region'].str.contains('Northern America')), 'Area'] = 'Aamerica'


    # Hago que Area sea la segunda columna
    column_to_move = df.pop("Area")
    df.insert(1, "Area", column_to_move)

    # Get list of areas
    areas = df.Area.unique()

    # Make numeric values floats
    df.iloc[:, 3:].astype(np.float64)

    # Calculate percentage change column
    df_shifted = df[['Country','REER']].groupby('Country').shift(1)
    df['Var'] = ((df['REER'] - df_shifted['REER']) / df_shifted['REER'])
    
    # Declare new variable and run regression
    df['Decade'] = (df.index.year // 10) * 10

    # Run the regression with fixed effects for region and decade
    result = smf.ols(formula='Var ~ C(Area) * C(Decade) - 1', data=df).fit()

    # Get list of areas
    areas = df.Area.unique()

    # Grafico todas las areas
    for area in areas:
        coefplot(result, area)