import streamlit as st
import Sheets

# Testing info
st.write("### 📊 Vista previa de los datos")
df = Sheets.get_table('Nodol')
st.dataframe(df)  # Display df

# df properties
st.write("### 🏷️ Columnas disponibles:")
st.write(df.columns.tolist())

selected_sheet = st.selectbox("Selecciona una pestaña 📄", Sheets.get_titles(df))