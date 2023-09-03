import sqlite3

from flask_restful import Resource, Api, reqparse
from app import app

api = Api(app)

user_parser = reqparse.RequestParser()

class MoviesResource(Resource):

    def put(self, movie_id):

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 

        user_parser.add_argument("name", type=str, required=False, help="Name is required.")
        user_parser.add_argument("imdb_score", type=str, required=False, help="imdb_score is required.")
        user_parser.add_argument("99popularity", type=str, required=False, help="popularity is required.")
        user_parser.add_argument("director", type=str, required=False, help="director is required.")
        user_parser.add_argument("genre", action="append", type=False, help="atleast one genre is required.")

        data = user_parser.parse_args()

        cursor.execute("SELECT * FROM Movies WHERE id = ?", (movie_id,))
        existing_data = cursor.fetchone()

        if existing_data is None:
            return jsonify({"message": "Movie not found"}), 404

        name = data['name'] if data['name'] else existing_data[1]
        imdb_score = data['imdb_score'] if data['imdb_score'] else existing_data[2]
        director = data['director'] if data['director'] else existing_data[3]
        popularity = data['99popularity'] if data['99popularity'] else existing_data[4]

        if type(director) == "string":
            cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
            matching_directors = cursor.fetchall()
            if not matching_directors:
                cursor.execute("INSERT INTO Director (name) VALUES (?)", (director,))
                director = cursor.lastrowid
            else:
                director = matching_directors[0][0]

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

    def delete(self, movie_id):
        try:
            # user_parser.add_argument("name", type=str, required=True, help="Name is required.")

            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            # data = user_parser.parse_args()

            # movie_name = data['name']
            # movie_name = movie_name.capitalize()

            cursor.execute("DELETE FROM MOVIES WHERE id = ?", (movie_id,))

            return {'message': 'moive deleted successfully'}, 200
        except Exception as error:
            return {'message': error}

class MovieResource(Resource):

    def post(self):

        user_parser.add_argument("name", type=str, required=True, help="Name is required.")
        user_parser.add_argument("imdb_score", type=str, required=True, help="imdb_score is required.")
        user_parser.add_argument("99popularity", type=str, required=True, help="popularity is required.")
        user_parser.add_argument("director", type=str, required=True, help="director is required.")
        user_parser.add_argument("genre", action="append", type=str, help="atleast one genre is required.")

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        data = user_parser.parse_args()

        movie_name = data['name']
        imdb_score = data['imdb_score']
        popularity = data['99popularity']
        director = data["director"]
        genre = data["genre"]

        director_id = 0
        popularity_id = 0
        imdb_score_id = 0
        movie_id = 0

        print(director, genre, movie_name, imdb_score, popularity)

        cursor.execute("SELECT * FROM GENRE WHERE genre = ?", (movie_name,))
        matching_movies = cursor.fetchall()
        if matching_movies:
            return {"message": "movie already exists"}, 409
        else:
            cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
            matching_directors = cursor.fetchall()
            if not matching_directors:
                cursor.execute("INSERT INTO Director (name) VALUES (?)", (director,))
                director_id = cursor.lastrowid
            else:
                director_id = matching_directors[0][0]

            cursor.execute("SELECT * FROM IMDB_SCORE WHERE score = ?", (imdb_score,))
            matching_score = cursor.fetchall()
            if not matching_score:
                cursor.execute("INSERT INTO IMDB_SCORE (score) VALUES (?)", (imdb_score,))
                imdb_score_id = cursor.lastrowid
            else:
                imdb_score_id = matching_score[0][0]

            cursor.execute("SELECT * FROM POPULARITY WHERE popularity = ?", (popularity,))
            matching_popularity = cursor.fetchall()
            if not matching_popularity:
                cursor.execute("INSERT INTO POPULARITY (popularity) VALUES (?)", (popularity,))
                popularity_id = cursor.lastrowid
            else:
                popularity_id = matching_popularity[0][0]

            cursor.execute("INSERT INTO movies (name, imdb_score, director, popularity) VALUES (?, ?, ?, ?)", (movie_name.capitalize(), imdb_score_id, director_id, popularity_id))
            movie_id = cursor.lastrowid

            for word in genre: 
                cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + word.capitalize() + "%",))
                matching_genre = cursor.fetchone()
                if matching_genre:
                    cursor.execute("INSERT INTO MOVIES_GENRE (genre_id, movie_id) VALUES (?, ?)", (matching_genre[0], movie_id))
        
        connection.commit()
        connection.close()


api.add_resource(MoviesResource, "/movies/<movie_id>")
api.add_resource(MovieResource, "/movie")
