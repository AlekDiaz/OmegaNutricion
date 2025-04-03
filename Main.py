import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Cargar credenciales desde Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]

# Definir los scopes correctos
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Crear credenciales con los scopes
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

# Autorizar con gspread
gc = gspread.authorize(creds)

# Intentar abrir la hoja de cálculo
try:
    spreadsheet = gc.open("Formula")
    sheet = spreadsheet.sheet1  # Usa la primera hoja (puedes cambiarlo si tienes varias)
    data = sheet.get_all_records()  # Obtener todos los datos como lista de diccionarios
    df = pd.DataFrame(data)  # Convertir a DataFrame de pandas
    
    st.success("✅ ¡Conexión exitosa a Google Sheets!")

    # Mostrar las primeras filas de la tabla
    st.write("### 📊 Vista previa de los datos")
    st.dataframe(df)  # Mostrar tabla interactiva en Streamlit

    # Mostrar nombres de las columnas
    st.write("### 🏷️ Columnas disponibles:")
    st.write(df.columns.tolist())

except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets: {e}")