from flask import jsonify
from flask_restful import Resource, Api, request, reqparse, abort
from flask_cors import cross_origin
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from .config import db
from datetime import datetime
from dotenv import load_dotenv
import pytz
import os
load_dotenv()

client = db()
google_sheet_job_description_table_name = os.getenv("google_sheet_job_description_table_name")
sheet1 = client.worksheet(google_sheet_job_description_table_name)  # Open the spreadhseet
IST = pytz.timezone('Asia/Kolkata')

class show(Resource):
    @cross_origin()
    def get(self):
         all_rows = sheet1.get_all_records()
         try:

                all_rows = sheet1.get_all_records()                
                return jsonify(all_rows)
                
         except Exception as e:
            return (e)
            