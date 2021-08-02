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
google_sheet_Candidate_table_name = os.getenv("google_sheet_Candidate_table_name")
sheet3 = client.worksheet(google_sheet_Candidate_table_name)  # Open the spreadhseet
#canvas_sheet = client.worksheet(google_sheet_Canvas_table_name)
IST = pytz.timezone('Asia/Kolkata')

class Candidate(Resource):
    @cross_origin()
    def get(self):
         all_rows = sheet3.get_all_records()
         user_data_parse = reqparse.RequestParser()

         user_data_parse.add_argument("userid", type=str, help="provide userid")
         #user_data_parse.add_argument("Email", type=str, help="provide Email")

        # storing request json((body) data in args
         args = user_data_parse.parse_args()
         userid = args['userid']

         try:

                all_rows = sheet3.get_all_records()
                # converting all data to dataframe
                google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

                if(userid != None):
                    User_data = google_sheet_all_records.loc[google_sheet_all_records['userid'] == int(userid)]
                    resp=[]
                    #User_data_by_title = google_sheet_all_records.loc[google_sheet_all_records['jid'] == int(jid)]
                    try:
                        resp.append(User_data.to_dict('records'))
                    except:
                        pass

                        # returning json data

                  
                    return jsonify(resp)
                else:
                    return jsonify({"response": "userid invalid"})
         except Exception as e:
            return (e)
            # return ({"response":"An error occurred"})
    @cross_origin()
    def post(self):
        
        user_data_parse = reqparse.RequestParser()

        user_data_parse.add_argument("userid", type=str, help='provide userid')
        user_data_parse.add_argument(
            "firstName", type=str, required=True, help="provide first name")
        user_data_parse.add_argument(
            "lastName", type=str, required=True, help="provide last name")
        user_data_parse.add_argument(
            "email", type=str, help="provide user email")
        user_data_parse.add_argument(
            "mobileNumber", type=str , help='provide mobile_no')
        user_data_parse.add_argument(
            "gender", type=str , help='provide gender')
        user_data_parse.add_argument(
            "hightet_qualification", type=str , help='provide hightet_qualification')
        user_data_parse.add_argument(
            "companyName", type=str , help='provide name_of_the_companies_worked')
        user_data_parse.add_argument(
            "expectedJob", type=str , help='provide expected_nature_of_job')
        user_data_parse.add_argument(
            "Address", type=str , help='provide address')
        user_data_parse.add_argument(
            "Address2", type=str , help='provide address2')
        user_data_parse.add_argument(
            "City", type=str , help='provide city')
        user_data_parse.add_argument(
            "State", type=str , help='provide state')
        user_data_parse.add_argument(
            "Pincode", type=str , help='provide zip ')
        user_data_parse.add_argument(
            "checkMe", type=str , help='provide checkmeout')
                #Canvas = "0,,"

        # storing request json((body) data in args
        args = user_data_parse.parse_args()
        IST = pytz.timezone('Asia/Kolkata')

        try:

            userid = args['userid']
            first_name = args['firstName']
            last_name = args['lastName']
            user_email = args['email']
            mobile_no = args['mobileNumber']
            gender = args['gender']
            hightet_qualification = args['hightet_qualification']
            name_of_the_companies_worked = args['companyName']
            expected_nature_of_job = args['expectedJob']
            address = args['Address']
            address2 = args['Address2']
            city = args['City']
            state = args['State']
            zip = args['Pincode']
            
            LastLogin = str(datetime.now(IST))

            #all_rows = sheet1.get_all_records()
            #google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

            #existed_Email = google_sheet_all_records.loc[google_sheet_all_records['Email'] == Email]

            # existed_UserId = google_sheet_all_records.loc[google_sheet_all_records['UserId'] == UserId]

            #existed_UserId_index = google_sheet_all_records.index[
                #google_sheet_all_records['Email'] == Email]
            #existed_UserId_index += 2

            if(first_name != 0):
                sheet3.append_row([userid,first_name,last_name,user_email,mobile_no,gender,hightet_qualification,name_of_the_companies_worked,expected_nature_of_job,address,address2,city,state,zip,LastLogin])
                return jsonify({"response": f"user added successfully for User -{first_name}"})
            #else:
                #sheet1.update(f"A{existed_UserId_index[0]}:F{existed_UserId_index[0]}", [
                              #[UserId, Email, Name,None,LastLogin,Admin]])
                # sheet1.update(
                #     f"E{existed_UserId_index[0]}:E{existed_UserId_index[0]}", [[LastLogin]])

               #return jsonify({"response": "Email existed"})
        except:
            return jsonify({"response": "An error occurred"})
    