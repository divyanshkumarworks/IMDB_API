from app import app

from flask_restful import Api, Resource, reqparse
import sqlite3
from helper.utility import *

api = Api(app)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str, required=True, help="Name is required.")
user_parser.add_argument("password", type=str, required=True, help="Password is required.")
user_parser.add_argument("role", type=str, required=True, help="Role is required")

class UserResrource(Resource):
	def post(self):

		connection = sqlite3.connect('database.db')
		cursor = connection.cursor() 
		
		user_parser.add_argument("id", type=str)
		data = user_parser.parse_args()

		if not is_valid_name(data["name"]):
			return {"message": "Invalid name"}, 400
		if not is_valid_password(data["password"]):
			return {"message": "Invalid password (should be at least 6 characters)"}, 400
		if data['role'] != "admin" and data['role'] != "user":
			return {"message": "role can either be user or admin"}

		cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", (data['name'].capitalize(), data['password'], data['role'].capitalize()))

		connection.commit()
		connection.close()

		return {'message': "user created successfully"}, 200

api.add_resource(UserResrource, '/user')


