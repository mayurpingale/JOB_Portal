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
google_sheet_Canvas_table_name = os.getenv(
    "FLASK_GOOGLE_SHEET_CANVAS_TABLE_NAME")
google_sheet_User_table_name = os.getenv("google_sheet_User_table_name")
sheet1 = client.worksheet(google_sheet_User_table_name)  # Open the workhseet

# to get User table data


class allUser(Resource):
    @cross_origin()
    def get(self):
       
        all_rows = sheet1.get_all_records()

        all_Canvas = client.worksheet(
            google_sheet_Canvas_table_name).get_all_records()

        all_User_data_to_return = []

        # converting all data to dataframe
        all_Canvas = pd.DataFrame.from_dict(all_Canvas)
        for response_data in all_rows:

            response_data['Canvas'] = response_data['Canvas'].split(",")
            # ----------------------------------------------------------------------------------
            resp = []

            if(len(response_data['Canvas']) >= 1):
                for canvasid in response_data['Canvas']:

                    try:
                        User_data_by_title = all_Canvas.loc[all_Canvas['CanvasId'] == int(
                            canvasid)]

                        resp.append(User_data_by_title.to_dict('records')[0])
                    except:
                        pass

                        # returning json data

                response_data['Canvas'] = resp
            all_User_data_to_return.append(response_data)
            # returning json data
        return jsonify(all_User_data_to_return)


class User(Resource):
    @cross_origin()
    def get(self):
        user_data_parse = reqparse.RequestParser()

        user_data_parse.add_argument("UserId", type=str, help="provide UserId")
        user_data_parse.add_argument("Email", type=str, help="provide Email")

        # storing request json((body) data in args
        args = user_data_parse.parse_args()
        UserId = args['UserId']
        Email = args['Email']

        try:

            all_rows = sheet1.get_all_records()
            # converting all data to dataframe
            google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

            if(Email != None):
                User_data = google_sheet_all_records.loc[google_sheet_all_records['Email'] == Email]
            else:
                User_data = google_sheet_all_records.loc[google_sheet_all_records['UserId'] == int(
                    UserId)]

            if(len(User_data) >= 1):
                response_data = User_data.to_dict('records')
                response_data[0]['Canvas'] = response_data[0]['Canvas'].split(
                    ",")
                # ----------------------------------------------------------------------------------
                all_rows = client.worksheet(
                    google_sheet_Canvas_table_name).get_all_records()
                # converting all data to dataframe
                google_sheet_all_records = pd.DataFrame.from_dict(all_rows)
                resp = []

                if(len(response_data[0]['Canvas']) >= 1):
                    for canvasid in response_data[0]['Canvas']:

                        try:
                            User_data_by_title = google_sheet_all_records.loc[google_sheet_all_records['CanvasId'] == int(
                                canvasid)]

                            resp.append(
                                User_data_by_title.to_dict('records')[0])
                        except:
                            pass

                        # returning json data

                    response_data[0]['Canvas'] = resp

                    # returning json data

                return jsonify(response_data[0])
            else:
                return jsonify({"response": "Email invalid"})
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

        user_data_parse.add_argument("UserId", type=str)
        user_data_parse.add_argument(
            "Name", type=str, required=True, help="provide Name")
        user_data_parse.add_argument(
            "Email", type=str, required=True, help="provide Email")
        user_data_parse.add_argument(
            "Canvas", type=str, help="provide Canvas")
        user_data_parse.add_argument(
            "Admin", type=str)

        #Canvas = "0,,"

        # storing request json((body) data in args
        args = user_data_parse.parse_args()
        IST = pytz.timezone('Asia/Kolkata')

        try:

            UserId = args['UserId']
            Name = args['Name']
            Email = args['Email']
            Canvas = args['Canvas']
            Admin = args['Admin']
            LastLogin = str(datetime.now(IST))

            all_rows = sheet1.get_all_records()
            google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

            existed_Email = google_sheet_all_records.loc[google_sheet_all_records['Email'] == Email]

            # existed_UserId = google_sheet_all_records.loc[google_sheet_all_records['UserId'] == UserId]

            existed_UserId_index = google_sheet_all_records.index[
                google_sheet_all_records['Email'] == Email]
            existed_UserId_index += 2

            if((len(existed_Email) == 0)):
                sheet1.append_row([UserId, Email, Name, Canvas, LastLogin,Admin])
                return jsonify({"response": f"user added successfully for Email-{Email}"})
            else:
                sheet1.update(f"A{existed_UserId_index[0]}:F{existed_UserId_index[0]}", [
                              [UserId, Email, Name,None,LastLogin,Admin]])
                # sheet1.update(
                #     f"E{existed_UserId_index[0]}:E{existed_UserId_index[0]}", [[LastLogin]])

                return jsonify({"response": "Email existed"})
        except:
            return jsonify({"response": "An error occurred"})

    @cross_origin()
    def delete(self):
        user_data_parse = reqparse.RequestParser()

        user_data_parse.add_argument(
            "Email", type=str, required=True, help="provide Email")

        args = user_data_parse.parse_args()

        #  storing data from url

        Email = args['Email']

        try:
            all_rows = sheet1.get_all_records()
            # converting all data to dataframe
            google_sheet_all_records = pd.DataFrame.from_dict(all_rows)

            # sorting data for requested userid
            google_sheet_all_records = google_sheet_all_records.loc[
                google_sheet_all_records['Email'] == Email]

            update_location_cell = google_sheet_all_records.index[
                google_sheet_all_records['Email'] == Email]

            if(len(update_location_cell) > 0):
                ccc = int(update_location_cell[0]) + 2

                sheet1.delete_rows(ccc)

                return jsonify({"response": f"User deleted successfully for Email-{Email}"})
            else:
                return jsonify({"response": "The Email not found or deleted already "})
        except:
            return jsonify({"response": f"The Email not found or deleted already"})
