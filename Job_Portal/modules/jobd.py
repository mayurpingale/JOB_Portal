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

#google_sheet_Canvas_table_name = os.getenv(
    #"FLASK_GOOGLE_SHEET_CANVAS_TABLE_NAME")
google_sheet_job_description_table_name = os.getenv("google_sheet_job_description_table_name")
sheet1 = client.worksheet(google_sheet_job_description_table_name)  # Open the spreadhseet
#canvas_sheet = client.worksheet(google_sheet_Canvas_table_name)
IST = pytz.timezone('Asia/Kolkata')

class job_description(Resource):
    @cross_origin()
    def get(self):
         all_rows = sheet1.get_all_records()
         user_data_parse = reqparse.RequestParser()

         user_data_parse.add_argument("jid", type=str, help="provide jid")
         #user_data_parse.add_argument("Email", type=str, help="provide Email")

        # storing request json((body) data in args
         args = user_data_parse.parse_args()
         jid = args['jid']

         try:

                all_rows = sheet1.get_all_records()
                # converting all data to dataframe
                google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

                if(jid != None):
                    User_data = google_sheet_all_records.loc[google_sheet_all_records['jid'] == int(jid)]
                    resp=[]
                    User_data_by_title = google_sheet_all_records.loc[google_sheet_all_records['jid'] == int(jid)]
                    try:
                        resp.append(User_data.to_dict('records'))
                    except:
                        pass

                        # returning json data

                  
                    return jsonify(resp)
                else:
                    return jsonify({"response": "jid invalid"})
         except Exception as e:
            return (e)
            # return ({"response":"An error occurred"})

    @cross_origin()
    def post(self):
        """
        when requested url http://127.0.0.1:5000/User?Userid=112&Username=any
        or any data.
        this function will add new user details to google sheet database.
        and return the responce.
        """
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

            #existed_Email = google_sheet_all_records.loc[google_sheet_all_records['Email'] == Email]

            # existed_UserId = google_sheet_all_records.loc[google_sheet_all_records['UserId'] == UserId]

            #existed_UserId_index = google_sheet_all_records.index[
                #google_sheet_all_records['Email'] == Email]
            #existed_UserId_index += 2

            if(jid != 0):
                sheet1.append_row([jid,name_of_the_company,website_link,logo_name,job_description,job_profile,job_category, LastLogin])
                return jsonify({"response": f"user added successfully for company-{website_link}"})
            #else:
                #sheet1.update(f"A{existed_UserId_index[0]}:F{existed_UserId_index[0]}", [
                              #[UserId, Email, Name,None,LastLogin,Admin]])
                # sheet1.update(
                #     f"E{existed_UserId_index[0]}:E{existed_UserId_index[0]}", [[LastLogin]])

               #return jsonify({"response": "Email existed"})
        except:
            return jsonify({"response": "An error occurred"})
                
                   
                    
                    
                 

                    
