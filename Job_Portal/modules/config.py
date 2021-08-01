import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
load_dotenv()

google_sheet_json_path = os.getenv("FLASK_GOOGLE_SHEET_JSON_PATH")


def db():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    details = ServiceAccountCredentials.from_json_keyfile_name(google_sheet_json_path, scope)

    client = gspread.authorize(details).open(os.getenv("Google_spreadSheet_name"))
    
    return client