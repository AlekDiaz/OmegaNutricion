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

# Main search function
def get_table() -> gspread.spreadsheet.Spreadsheet:
    try:
        spreadsheet = gc.open('Formula')
        return spreadsheet

    except Exception as e:
        return e

def get_worksheet(spreadsheet, key) -> pd.DataFrame:  
        sheet = spreadsheet.worksheet(key)  # First Sheets
        data = sheet.get_all_records()  # Get all data **[{}{}]**
        df = pd.DataFrame(data)  # Cast data to Pandas DataFrame

        return df

def get_titles(spreadsheet):
     # Obtener lista de pestañas
    worksheets = spreadsheet.worksheets()
    sheet_names = [ws.title for ws in worksheets]

    return sheet_names[4:]