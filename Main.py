import streamlit as st
import Sheets

# Testing info
st.write("### 📊 Vista previa de los datos")

if not Sheets.get_table('Nodol'):
    st.write("La tabla no se pudo encontrar")
else:
    df = Sheets.get_table('Nodol')
    st.dataframe(df)  # Display df

    # df properties
    st.write("### 🏷️ Columnas disponibles:")
    st.write(df.columns.tolist())