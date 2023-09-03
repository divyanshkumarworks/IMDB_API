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

1. `POST /movies` Create a new movie. (Request body should contain the resource data in JSON format.)
2. `DELETE /movies/<id>` Delete a movie with the specified ID.
3. `PUT /movies/<id>` Update an existing movie identified by its ID. (Request body should contain the updated resource data in JSON format.)
4. `GET /movies/search` Search for existing movies using various filters.
## Scalablity Challenges
