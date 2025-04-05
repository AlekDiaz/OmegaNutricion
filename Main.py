import streamlit as st
import Sheets

# Testing info
st.write("### 📊 Vista previa de los datos")
df = Sheets.get_table()

selected_sheet = st.selectbox("Selecciona una pestaña 📄", Sheets.get_titles(df))