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

class job_description(Resource):
    @cross_origin()
    def get(self):
         all_rows = sheet1.get_all_records()
         user_data_parse = reqparse.RequestParser()

         user_data_parse.add_argument("job_category", type=str, help="provide job_category")
        
        # storing request json((body) data in args
         args = user_data_parse.parse_args()
         job_category = args['job_category']

         try:

                all_rows = sheet1.get_all_records()
                # converting all data to dataframe
                google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

                if( job_category != None):
                    User_data = google_sheet_all_records.loc[google_sheet_all_records['job_category'] == job_category]
                    resp=[]
                    User_data_by_title = google_sheet_all_records.loc[google_sheet_all_records['job_category'] == job_category]
                    try:
                        resp.append(User_data.to_dict('records'))
                    except:
                        pass

                        # returning json data

                  
                    return jsonify(resp)
                else:
                    return jsonify({"response": "job_category invalid"})
         except Exception as e:
            return (e)
            # return ({"response":"An error occurred"})

    @cross_origin()
    def post(self):
        
        user_data_parse = reqparse.RequestParser()

        user_data_parse.add_argument("jid", required=True, type=str)
        user_data_parse.add_argument(
            "name_of_the_company", type=str, required=True, help="provide name_of_the_company")
        user_data_parse.add_argument(
            "website_link", type=str, required=True, help="provide website_link")
        user_data_parse.add_argument(
            "logo_name", type=str, help="provide logo_name")
        user_data_parse.add_argument(
            "job_description", type=str , help='provide job descriptions')
        user_data_parse.add_argument(
            "job_profile", type=str , help='provide job_profile')
        user_data_parse.add_argument(
            "job_category", type=str , help='provide job_category')
        #Canvas = "0,,"

        # storing request json((body) data in args
        args = user_data_parse.parse_args()
        IST = pytz.timezone('Asia/Kolkata')

        try:

            jid = args['jid']
            name_of_the_company = args['name_of_the_company']
            website_link = args['website_link']
            logo_name = args['logo_name']
            job_description = args['job_description']
            job_profile = args['job_profile']
            job_category = args['job_category']
            LastLogin = str(datetime.now(IST))

            all_rows = sheet1.get_all_records()
            google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

            

            if(jid != 0):
                sheet1.append_row([jid,name_of_the_company,website_link,logo_name,job_description,job_profile,job_category, LastLogin])
                return jsonify({"response": f"user added successfully for company-{website_link}"})
            
        except:
            return jsonify({"response": "An error occurred"})
                
                   
                    
                    
                 

                    
