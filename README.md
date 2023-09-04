# IMDB_API

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

## Getting Started: 🚀

### Prerequisites 📋
Before running the application, ensure you have the following installed:

- Python (version 3.6 or higher)
- Flask (version 2.0.0 or higher)
- any sqlite3 Database Management Tool for data interaction (ex:- DB Browser) 

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Installation
1. Clone this repository
 ```bash
 https://github.com/divyanshkumarworks/IMDB_API.git
 ```
2. go inside clone folder
 ```bash
 cd IMDB_API
```
3. Create a Virtual Environment
 ```bash
 python -m venv venv
 ```
4. Activate the environment
 ```bash
 source /venv/bin/activate
 ``` 
5. install all dependencies:
```bash
python -m pip install -r requirements.txt
```

6. Run the Flask app.
```bash
flask run
```
The application will be accessible at http://127.0.0.1:5000.

## API Endpoints

The following API endpoints are available:

1. `POST /user/register` for signUp or creating a new user. (Request body should contain the resource data in JSON format.)
```bash
{
   "name": "XYZ",
   "password: 123,
   "role": Admin/User
}
```
2. `POST /user/authenticate` for Authenticating whether user exists or is admin or not. (Request body should contain the resource data in JSON format.)
```bash
{
   "name": "XYZ",
   "password: 123,
}
```
3. `POST /movies` Stores a new movie. (Request body should contain the resource data in JSON format.)
```bash
resource required for creating new movie data
{
    "99popularity": ,
    "name": "",
    "imdb_score": ,
    "genre": [""],
    "director": ""
}
```
4. `DELETE /movies/<id>` Delete a movie with the specified ID.
```bash
Ex:- http://127.0.0.1:5000/movies/1 will delete the existing movie for the table with ID 1.
```
5. `PUT /movies/<id>` Update an existing movie identified by its ID. (Request body should contain the updated resource data in JSON format.)
```bash
resource required for creating new movie data
{
    "99popularity": ,
    "name": "",
    "imdb_score": ,
    "genre": [""],
    "director": ""
}
```
Note:- user can provide or update any of the above data to change otherwise it adds the existing data to the table

6. `GET /movies/search/...` Search for existing movies using various filters.

**Getting movies by name**
```bash
http://127.0.0.1:5000/movies/search
{
    "name": ""
}
```

**Getting movies by director**
```bash
http://127.0.0.1:5000/movies/search?director=XYZ
```

**Getting movies by genre**
```bash
http://127.0.0.1:5000/movies/search?genre=XYZ&genre=ABC
```

**Getting movies by sort**
By default the movies are sorted by popularity but user can sorted with imdb_score and id.
```bash
http://127.0.0.1:5000/movies/search?sort_by=id
```

**Getting movies by Order(ascending or descending)**
```bash
http://127.0.0.1:5000/movies/search?order=asc
```
**Note**: user can combine these filters to generate customize advance search query
## Scalablity Challenges
