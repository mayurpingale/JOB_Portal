# from Job_Portal.modules.jobd import job_description
#from typing_extensions import Required
from flask import jsonify
from flask_restful import Resource, Api, request, reqparse, abort
from flask_cors import cross_origin
import gspread
import smtplib, ssl
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pandas.core.indexing import need_slice
from .config import db
from datetime import datetime
from dotenv import load_dotenv
import pytz
import os
load_dotenv()

client = db()
google_sheet_job_description_table_name = os.getenv("google_sheet_job_description_table_name")
sheet1 = client.worksheet(google_sheet_job_description_table_name)
google_sheet_Candidate_table_name = os.getenv("google_sheet_Candidate_table_name")
sheet3 = client.worksheet(google_sheet_Candidate_table_name)  # Open the spreadhseet
IST = pytz.timezone('Asia/Kolkata')

class Candidate(Resource):
    @cross_origin()
    def get(self):
         all_rows = sheet3.get_all_records()
         user_data_parse = reqparse.RequestParser()

         user_data_parse.add_argument("userid", type=str, help="provide userid")
         
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
        user_data_parse.add_argument(
            "jid", type=str  , help='provide jid')
        user_data_parse.add_argument(
            "Resume", type=str  , help='provide Resume')   
        #this is resume link ...fetch from frontend


        args = user_data_parse.parse_args()
        IST = pytz.timezone('Asia/Kolkata')            
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
        jid=args['jid']
        Resume=args['Resume']
        LastLogin = str(datetime.now(IST))
           

        # storing request json((body) data in args
        args = user_data_parse.parse_args()
        IST = pytz.timezone('Asia/Kolkata')
        all_rows = sheet1.get_all_records()
        google_sheet_all_records = pd.DataFrame.from_dict(all_rows)
        if(jid != None):
                User_data = google_sheet_all_records.loc[google_sheet_all_records['jid'] ==int(jid)]
        if(len(User_data) >= 1):
                response_data = User_data.to_dict('records')
                job_descriptions=response_data[0]['job_description']
                name_of_the_company=response_data[0]['name_of_the_company']
                job_profile=response_data[0]['job_profile']
                job_category=response_data[0]['job_category']
                company_mail=response_data[0]['website_link']
        #resp=[]
        # above we retrive data from job description table by job id and store in above variable so use this for email purpose           
               
        # resp.append(job_descriptions)
        # resp.append(name_of_the_company)
        # resp.append(job_profile)
        # resp.append(job_category)

        # only thing is that change website link in sheet to mail then test it for bcc mail purpose
        
        try:
            #msg =

            
            if(first_name != 0):
                sheet3.append_row([userid,first_name,last_name,user_email,mobile_no,gender,hightet_qualification,name_of_the_companies_worked,expected_nature_of_job,address,address2,city,state,zip,LastLogin])
                port = 587  # For starttls
                smtp_server = "smtp.gmail.com"
                sender_email = "testjobportal01@gmail.com"
                receiver_email = user_email
                password = "testingjobportal"
                message =  """Subject: JOB-PORTAL  \nNEW APPLICATION\nName :  """+ first_name + Resume #+ """  """+ last_name + """ Gender"""+ gender + """\nQualification : """ + hightet_qualification + """\nApplying For : """ + job_category + """\nJob id : """ + jid + """\n Job Description : """ + job_descriptions + """\nCompany Name :""" + name_of_the_company + """\n\n Contact Information \nEmail : """ + user_email + """\nMobile : """ + mobile_no + """\nAddress : """ + address + """, """ + address2 + """\nCity : """ + city + """\nState : """ + state + """\nPincode : """ + zip

                context = ssl.create_default_context()
                # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                #     server.login(sender_email, password)
                #     server.sendmail(sender_email, receiver_email, message)
                with smtplib.SMTP(smtp_server, port) as server:
                     server.ehlo()  # Can be omitted
                     server.starttls(context=context)
                     server.ehlo()  # Can be omitted
                     server.login(sender_email, password)
                     server.sendmail(sender_email, receiver_email, message)
                 #return jsonify(resp)
                return jsonify({"response": f"user added successfully for User -{first_name}"})
            
        except Exception as e:
            #return jsonify({"response": "An error occurred"})
            
            return (e)
    