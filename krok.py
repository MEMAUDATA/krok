# https://epieos.com/pricing

import streamlit as st
import pandas as pd
import re
import numba
import subprocess
import sys

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
with open('krok.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Hearing data title
st.html("<h1 style='text-align:center;'>Krok</h1>")
#color:#2B176C
name, authentication_status, username = authenticator.login('main')

if authentication_status:

    if username == 'krok': # credentials used for demo
        # Title section written with html
        st.html("<p style='text-align:center;'> Analyse économique annuelle et potentiellement global</p>")
        st.html("""<div style="height: 10px;"></div>""")    
        # upload section written with html
        xmlfiles = st.file_uploader("Upload file(s) in .csv", accept_multiple_files=True,type=['.csv'])
        st.html("""<div style="height: 10px;"></div>""") 
        
    authenticator.logout('Logout','main')
elif authentication_status == False:
    st.error('Username/password is incorrect')





