# Krok annual incommes' analysis
# NV, Toulouse,07/2025

import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers
import os
import pandas as pd
import numpy as npsource

from modules.synthesis import synthesis

# Désactive X-Frame-Options (à utiliser avec prudence !)
def _set_websocket_headers():
    headers = _get_websocket_headers()
    if "X-Frame-Options" in headers:
        del headers["X-Frame-Options"]
    return headers

st.set_page_config(layout="wide")




st.html("<h1 style='text-align:center;color:#22573b;'>Krok</h1>")
#color:#2B176C

 #Title section written with html
st.html("<p style='text-align:center;color:#22573b;'> Analyse économique à plusieurs niveaux afin d'observer l'évolution du CA.<br> Il faut nommer chaque fichier en fonction de l'année (ex: 2023.xls) </p>")
st.html("""<div style="height: 10px;"></div>""")    
# upload section written with html
csvfiles = st.file_uploader("Upload file(s) in .csv,.xls,.xlsx", accept_multiple_files=True,type=['.csv','.xls','xlsx'])
st.html("""<div style="height: 10px;"></div>""") 


#  Button to trigger processing
if st.button("Process", key="process_button"):        

    for file_name in csvfiles:
        file = pd.read_excel(file_name,sheet_name=None)
        income,df1 = synthesis(file)
        #print((income))
        file_stem, _ = os.path.splitext(file_name.name)
        st.subheader(f"Année {file_stem}")
        st.table(income)
