import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Cargar credenciales desde secrets
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(creds_dict)

# Conectarse a Google Sheets
gc = gspread.authorize(creds)
spreadsheet = gc.open("Nombre_de_tu_Google_Sheet")

st.write("¡Conexión exitosa a Google Sheets!")
