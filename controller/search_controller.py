from app import app

from flask_restful import Api, Resource, reqparse
import sqlite3

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('director')
parser.add_argument('genre')
parser.add_argument('sort_by', default='popularity')
parser.add_argument('order', default='desc')

class SearchResource(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor() 

            # Base query
            query = "SELECT * FROM Movies WHERE "
            values = []
            # Parameters for filtering and sorting
            filters = []
            sort_by = args['sort_by']
            order = args['order']

            # Filtering logic
            if args['director']:
                director = args['director']
                filters.append(f"director = ?")
                cursor.execute("SELECT * FROM Director WHERE name = ?", (director,))
                matching_query = cursor.fetchone()
                values.append(matching_query[0])

            print(query)

            if args['genre']:
                print(args['genre'])
                cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + args['genre'] + "%",))
                matching_query = cursor.fetchone()
                print(matching_query)
                values.append(matching_query[0])
                filters.append(f"AND EXISTS (SELECT * FROM MOVIES_GENRE WHERE MOVIES_GENRE.movie_id = MOVIES.id AND MOVIES_GENRE.genre_id = (?))")

            print(query)

            # Apply filters to the query
            if filters:
                query += " AND ".join(filters)

            print(query)

            # Sorting logic
            if sort_by in ('popularity', 'imdb_score'):
                query += f" ORDER BY {sort_by} {order}"

            print(query, values)

            cursor.execute(query, values)
            movies = cursor.fetchall()

            # Close the database connection
            connection.close()

            data = {
            "movies": []
            }

            for item in movies:
                print(item)
                data["movies"].append(
                        {
                            "id": item[0],
                            "name": item[1],
                            "imdb_score": item[2],
                            "director": item[3],
                            "popularity": item[4]
                        }
                    )

            return {"data": data}

        except Exception as e:
            return {'error': str(e)}, 500

api.add_resource(SearchResource, '/movies/search')