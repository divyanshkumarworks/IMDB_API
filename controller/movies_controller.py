import sqlite3

from flask_restful import Resource, Api, reqparse
from app import app
from helper.utility import jwt_token_required

api = Api(app)

user_parser = reqparse.RequestParser()  
user_parser.add_argument("name", type=str, required=False, help="Name is required.")
user_parser.add_argument("imdb_score", type=str, required=False, help="imdb_score is required.")
user_parser.add_argument("99popularity", type=str, required=False, help="popularity is required.")
user_parser.add_argument("director", type=str, required=False, help="director is required.")
user_parser.add_argument("genre", action="append", type=False, help="atleast one genre is required.")

class MoviesResource(Resource):

    @jwt_token_required
    def put(self, movie_id):

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 

        data = user_parser.parse_args()

        cursor.execute("SELECT * FROM Movies WHERE id = ?", (movie_id,))
        existing_data = cursor.fetchone()

        if existing_data is None:
            return {"message": "Movie not found"}, 404

        name = data['name'] if data['name'] else existing_data[1]
        imdb_score = data['imdb_score'] if data['imdb_score'] else existing_data[2]
        director = data['director'] if data['director'] else existing_data[3]
        popularity = data['99popularity'] if data['99popularity'] else existing_data[4]

        if data["director"]:
            cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
            matching_directors = cursor.fetchone()
            if not matching_directors:
                cursor.execute("INSERT INTO Director (name) VALUES (?)", (director,))
                director = cursor.lastrowid
            else:
                director = matching_directors[0]

        if data['imdb_score'] :
            cursor.execute("SELECT * FROM IMDB_SCORE WHERE score = ?", (imdb_score,))
            matching_score = cursor.fetchall()
            if not matching_score:
                cursor.execute("INSERT INTO IMDB_SCORE (score) VALUES (?)", (imdb_score,))
                imdb_score = cursor.lastrowid
            else:
                imdb_score = matching_score[0][0]

        if data['99popularity']:
            cursor.execute("SELECT * FROM POPULARITY WHERE popularity = ?", (popularity,))
            matching_popularity = cursor.fetchall()
            if not matching_popularity:
                cursor.execute("INSERT INTO POPULARITY (popularity) VALUES (?)", (popularity,))
                popularity = cursor.lastrowid
            else:
                popularity = matching_popularity[0][0]


        cursor.execute(
            "UPDATE Movies SET popularity = ?, name = ?, director = ?, imdb_score = ? WHERE id = ?",
            (popularity, name, director, imdb_score, movie_id)
        )

        if data['genre']:
            cursor.execute("DELETE FROM MOVIES_GENRE WHERE movie_id = ?", (movie_id,))
            for word in data['genre']: 
                cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + word.capitalize() + "%",))
                matching_genre = cursor.fetchone()
                if matching_genre:
                    cursor.execute("INSERT INTO MOVIES_GENRE (genre_id, movie_id) VALUES (?, ?)", (matching_genre[0], movie_id))

        connection.commit()
        connection.close()

        return {"message": "Movie updated successfully"}, 200

    @jwt_token_required
    def delete(self, movie_id):
        try:
            print(movie_id)
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            cursor.execute("DELETE FROM MOVIES WHERE id = ?", (movie_id,))

            connection.commit()
            connection.close()

            return {'message': 'moive deleted successfully'}, 200
        except Exception as error:
            return {'message': error}

    @jwt_token_required
    def post(self):

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        data = user_parser.parse_args()

        movie = data['name']
        imdb_score = data['imdb_score']
        popularity = data['99popularity']
        director = data["director"]
        genre = data["genre"]

        print(director, genre, movie, imdb_score, popularity)

        cursor.execute("SELECT * FROM GENRE WHERE genre = ?", (movie,))
        matching_movies = cursor.fetchall()
        if matching_movies:
            return {"message": "movie already exists"}, 409
        else:
            cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
            matching_directors = cursor.fetchall()
            if not matching_directors:
                cursor.execute("INSERT INTO Director (name) VALUES (?)", (director,))
                director = cursor.lastrowid
            else:
                director = matching_directors[0][0]

            cursor.execute("SELECT * FROM IMDB_SCORE WHERE score = ?", (imdb_score,))
            matching_score = cursor.fetchall()
            if not matching_score:
                cursor.execute("INSERT INTO IMDB_SCORE (score) VALUES (?)", (imdb_score,))
                imdb_score = cursor.lastrowid
            else:
                imdb_score = matching_score[0][0]

            cursor.execute("SELECT * FROM POPULARITY WHERE popularity = ?", (popularity,))
            matching_popularity = cursor.fetchall()
            if not matching_popularity:
                cursor.execute("INSERT INTO POPULARITY (popularity) VALUES (?)", (popularity,))
                popularity = cursor.lastrowid
            else:
                popularity = matching_popularity[0][0]

            cursor.execute("INSERT INTO movies (name, imdb_score, director, popularity) VALUES (?, ?, ?, ?)", (movie.capitalize(), imdb_score, director, popularity))
            movie = cursor.lastrowid

            for word in genre: 
                cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + word.capitalize() + "%",))
                matching_genre = cursor.fetchone()
                if matching_genre:
                    cursor.execute("INSERT INTO MOVIES_GENRE (genre_id, movie_id) VALUES (?, ?)", (matching_genre[0], movie))
        
        connection.commit()
        connection.close()

api.add_resource(MoviesResource, "/movies/<movie_id>")
