# Krok annual incommes' analysis
# NV, Toulouse,07/2025

import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from modules.synthesis import synthesis
from modules.combine_plot import combine_plot
from modules.plot_unique_year import plot_unique_year


from modules.synthesis import synthesis
from modules.combine_plot import combine_plot
from modules.plot_unique_year import plot_unique_year

# Page configuration
st.set_page_config(page_title="Krok Analysis", layout="wide", initial_sidebar_state="expanded")

# Title section
st.markdown("<h1 style='text-align:center;color:#22573b;'>Krok</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#22573b;'>Analyse économique à plusieurs niveaux afin d'observer l'évolution du CA.<br>Il faut nommer chaque fichier en fonction de l'année (ex: 2023.xls)</p>", unsafe_allow_html=True)
st.divider()


# Load data
def load_data():
    csvfiles = st.sidebar.file_uploader("Upload files", accept_multiple_files=True,type=['.csv','.xls','xlsx'])
    return csvfiles

# table_data
def table_data(df,filename):

    num_cols = len(df.columns)
    columnwidths = [1] * num_cols 
    fig = go.Figure(
                data=[go.Table(
                    columnwidth = columnwidths,
                    header=dict(
                        values=[col.upper() for col in df.columns],
                        fill_color='lightgrey',
                        align='center'
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color='white',
                        align='center'
                    )
                )]
            )
    fig.update_layout(
    title={
        "text": filename,
        "x": 0.5,          # center the title
        "xanchor": "center",
        "yanchor": "top"
    }
)        

    st.plotly_chart(fig)

def best_days_per_year(csvfiles):

    def find_annual_growth(file):
        file_stem, _ = os.path.splitext(file.name)
        file = pd.read_excel(file, sheet_name=None)
        income, _ = synthesis(file)
        st.metric(label=f"CA {file_stem}", value=f"{income['sum'].sum():,.2f} €")

    n = len(csvfiles)

    if n >= 3:
        # Create one column per file
        cols = st.columns(n)
        for i, file in enumerate(csvfiles):
            with cols[i]:
                find_annual_growth(file)

    elif n == 2:
        # Create 3 columns, use left and right to center content
        cols = st.columns(4)
        with cols[1]:
            find_annual_growth(csvfiles[0])
        with cols[2]:
            find_annual_growth(csvfiles[1])

    elif n == 1:
        # Create 3 columns, use middle one
        cols = st.columns(3)
        with cols[1]:
            find_annual_growth(csvfiles[0])

def main():
    """
    Main Krok app.
    """
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("File uploading")
    csvfiles = load_data()

    #  Button to trigger processing
    if st.sidebar.button("Process", key="process_button"):

        # Plot best days of the years
        best_days_per_year(csvfiles)

        results = [] # for storage
        df_list = [] 
        for file_name in csvfiles:
            file = pd.read_excel(file_name,sheet_name=None)
            income,df = synthesis(file)
            file_stem, _ = os.path.splitext(file_name.name)
            results.append((file_stem, income))
            df_list.append(df)


        tab1, tab2,tab3 = st.tabs(["Figure regroupant toutes les années", "Data par année", "Figure par année"])

        with tab1:
            col1, col2, col3 = st.columns([0.2, 0.8, 0.2])  # center column wider
            with col2:
                overall_fig = combine_plot(df_list)
                st.pyplot(overall_fig,clear_figure=True)
            

        with tab2:
            for file_stem, income in results:
                     table_data(income,file_stem)

        with tab3:
            col1, col2, col3 = st.columns([0.3, 0.7, 0.3])  # center column wider
            with col2:
                    for df in df_list:
                        fig = plot_unique_year(df)   # returns a Matplotlib figure
                        st.markdown(
                            "<div style='margin-top:50px;'></div>",
                            unsafe_allow_html=True
                        )
                        st.pyplot(fig, clear_figure=True)

                    

            

   
if __name__ == '__main__':
    main()
