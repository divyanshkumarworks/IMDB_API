from app import app
from flask import make_response
from flask_restful import Api, Resource, reqparse
import jwt
api = Api(app)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str, required=True, help="Name is required.")
user_parser.add_argument("password", type=str, required=True, help="Password is required")

class AuthenticateResource(Resource):
	def post(self):
		try:
			data = user_parser.parse_args()		

			name = data["name"].capitalize()
			password = data["password"].capitalize()

			payload_data = {  
				  "sub": "1",  
				  "name": name,  
				  "password": password 
				}  
				
			token = jwt.encode(
				payload=payload_data,
				key = "my_secret_key"  
				)

			response = make_response({'token': token})
			response.set_cookie('jwt_token', token)
			return response
		except Exception as error:
			return {"mesage": error}

api.add_resource(AuthenticateResource, '/user/authenticate')