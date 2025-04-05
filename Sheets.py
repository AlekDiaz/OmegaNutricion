import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from streamlit import secrets

# Streamlit Creds
creds_dict = secrets["gcp_service_account"]

# Direct Access, scopes required (Sheets & Drive)
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# OAuth2 creds for service accounts
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

# Authorize gspread
gc = gspread.authorize(creds)

# Main search function to get the spreadsheet
def get_table() -> gspread.spreadsheet.Spreadsheet:
    try:
        spreadsheet = gc.open('Formula')  # Open the "Formula" spreadsheet
        # Verificar si la variable 'spreadsheet' es del tipo adecuado
        if isinstance(spreadsheet, gspread.Spreadsheet):  # Cambiado de 'gspread.models.Spreadsheet' a 'gspread.Spreadsheet'
            return spreadsheet
        else:
            raise TypeError("The returned object is not a valid Spreadsheet object.")
    except Exception as e:
        return f"Error in get_table: {str(e)}"


# Function to load all sheets data into session state
def load_all_sheets() -> dict:
    try:
        spreadsheet = get_table()  # Get the "Formula" spreadsheet
        if isinstance(spreadsheet, str):  # In case of error (spreadsheet is a string with the error)
            raise ValueError(spreadsheet)
        
        sheet_titles = get_titles(spreadsheet)  # Get the list of sheet names
        sheets_data = {}

        # Load each sheet into a dictionary with the sheet name as key
        for title in sheet_titles:
            df = get_worksheet(spreadsheet, title)
            sheets_data[title] = df

        return sheets_data

    except Exception as e:
        return f"Error in load_all_sheets: {str(e)}"

# Function to get the data from a specific worksheet as a pandas DataFrame
def get_worksheet(spreadsheet, key) -> pd.DataFrame:
    try:
        sheet = spreadsheet.worksheet(key)  # Get the worksheet by its name
        data = sheet.get_all_records()  # Get all records from the sheet as a list of dictionaries
        df = pd.DataFrame(data)  # Convert to pandas DataFrame
        return df
    except Exception as e:
        return f"Error in get_worksheet: {str(e)}"

# Function to get all sheet names
def get_titles(spreadsheet):
    try:
        worksheets = spreadsheet.worksheets()  # Get all worksheets
        sheet_names = [ws.title for ws in worksheets]  # Extract sheet names
        return sheet_names
    except Exception as e:
        return f"Error in get_titles: {str(e)}"
