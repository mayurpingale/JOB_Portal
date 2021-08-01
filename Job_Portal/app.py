from modules.candidate import Candidate
from flask import Flask
from flask_restful import Resource, Api, request
from flask_cors import CORS, cross_origin

# for kanban canvas and car details
#from modules.canvas_kanban import Canvas_card, cardData, Create_canvas, Canvas_users, AllTables, allcards, allCanvas, SheetPerm, Export, BoardCard
# to add user
#from modules.UserAdd import User, allUser
from modules.jobd import job_description 
from modules.candidate import Candidate
from modules.show import show
# for card type
#from modules.card import Card_Type
# for .env file
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app, resources={r"/*": {"origins": ["https://karyam.herokuapp.com/"]}})

api = Api(app)


# routing
api.add_resource(show,'/')
api.add_resource(job_description,'/jobd')
api.add_resource(Candidate,'/candidate')

if __name__ == '__main__':
    if(os.getenv("enviornment_production") == "True"):
        app.run(host='0.0.0.0', port=80)
    else:
        app.run(debug=True)
