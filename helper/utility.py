import jwt
import sqlite3
from flask import request, jsonify, make_response

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_name(name):
    return bool(name.strip())

def is_valid_password(password):
    return len(password) >= 2

def jwt_token_required(func):

    def decorator(*args, **kwargs):

        token = request.cookies.get('jwt_token')

        print("decorator is working")

        if token:   
            payload = jwt.decode(
                token,
                key="my_secret_key",
                algorithms=["HS256"]
                )
           
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor() 

            name = payload["name"]
            password = payload["password"]

            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name.capitalize(), password))
            user = cursor.fetchone()
            print(user)
            if not user:
                return {"message": "invalid username or password"}

            if user[3] == "User":
                return {"message": "user is not admin"}
            connection.commit()
            connection.close()

            func1 = func(*args, **kwargs)
            return func1

        else:
            return {"message": "token not found"}, 401 

    return decorator