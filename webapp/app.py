from webapp import all_regions, one_region, references, regression
import streamlit as st

def run_app():
    st.title('Real Exchange Rate')
    PAGES = {
            "Single Region": one_region,
            "All Regions": all_regions,
            "References": references
        }

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv('REER/reer/data/REER_annual.csv')

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


    page.run_app(df)