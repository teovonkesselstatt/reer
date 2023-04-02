from webapp import all_regions, one_region, references, regression
import streamlit as st

def run_app():
    st.title('Real Exchange Rate')
    PAGES = {
            "Single Region": one_region,
            "All Regions": all_regions,
            "Regression Results!": regression,
            "References": references
        }

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    page.run_app()