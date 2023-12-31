from app import app

from flask_restful import Api, Resource, reqparse
import sqlite3

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('director')
parser.add_argument('genre', type=str, action='append')
parser.add_argument('sort_by', default='popularity')
parser.add_argument('order', default='desc')
parser.add_argument('name', type=str)

class SearchResource(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor() 

            query = """SELECT * FROM MOVIES JOIN MOVIES_GENRE ON MOVIES.id = MOVIES_GENRE.movie_id JOIN GENRE ON MOVIES_GENRE.genre_id = GENRE.id JOIN Director ON MOVIES.director = Director.id JOIN IMDB_SCORE ON MOVIES.imdb_score = IMDB_SCORE.id JOIN POPULARITY ON MOVIES.popularity = POPULARITY.id"""
            
            
            values = []
            filters = []
            sort_by = args['sort_by']
            order = args['order']



            if args['name']:
                print(args['name'])
                movie = args['name']
                filters.append(f"MOVIES.name LIKE ?")
                values.append("%" + movie + "%")

            print(query)
            if args['director']:
                director = args['director']
                filters.append(f"director = ?")
                cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
                matching_query = cursor.fetchone()
                values.append(matching_query[0])

            print(query)

            if args['genre']:
                print(args['genre'])
                print(type(args['genre']))
                genre_condition = " OR ".join(["GENRE.genre LIKE ?" for _ in args['genre']])
                filters.append(f"({genre_condition})")
                for item in args['genre']:
                    values.append("%" + item + "%")

            print(query)

            if filters:
                query += " WHERE " + " AND ".join(filters)
            else:
                query += " WHERE 1"

            print(query)
            print(sort_by)

            if sort_by == "popularity":
                query += f" ORDER BY POPULARITY.{sort_by} {order.upper()}"

            if sort_by == "imdb_score":
                query += f" ORDER BY IMDB_SCORE.score {order.upper()}"
            
            if sort_by == "id":
                query += f" ORDER BY MOVIES.{sort_by} {order.upper()}"

            print(query)
            cursor.execute(query, values)
            movies = cursor.fetchall()
            
            connection.close()

            data = {
            "movies": []
            }

            for item in movies:
                data["movies"].append(
                        {
                            "id": item[0],
                            "name": item[1],
                            "imdb_score": item[12],
                            "director": item[10],
                            "popularity": item[14],
                            "genre": item[8]
                        }
                    )

            return {"data": data}

        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(SearchResource, '/movies/search')