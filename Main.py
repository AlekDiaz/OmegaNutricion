import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Authenticate using Streamlit Secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "Your Sheet Name"  # Replace with your actual Google Sheet name
worksheet = client.open(SHEET_NAME).sheet1  # Access the first sheet

# Load data into a DataFrame
def load_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Display data in Streamlit
st.title("Data Analysis Platform 🚀")
st.subheader("Current Data in Google Sheets")

df = load_data()
st.dataframe(df)

# Add new data from the UI
st.subheader("Add New Data")

columns = df.columns.tolist()  # Get column names from the sheet

new_data = []
for col in columns:
    new_data.append(st.text_input(f"Enter {col}", ""))

if st.button("Add Data"):
    if all(new_data):  # Ensure no empty fields
        worksheet.append_row(new_data)
        st.success("Data successfully added 🚀")
        st.experimental_rerun()  # Reload the app to show updated data
    else:
        st.error("All fields are required.")
