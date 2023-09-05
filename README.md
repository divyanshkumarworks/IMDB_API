# IMDB_API

## About 

### Introduction
The IMDb-like system is a web-based platform that provides users with access to a database of movies and related information. It allows users to browse, search for, and interact with movie data. This documentation provides an overview of the system's architecture, features, and API endpoints.

The backend consists of a Flask-based RESTful API, SQLite database for data storage, and various components for authentication, authorization, and search functionality.

## Features 

### User Features
**User Authentication:**

Users can register and log in.

**1. Movie Listings:**

Users can view a list of movies and TV shows, including details such as title, director, genre, IMDb score, and popularity.

**2. Search Functionality:**

Robust search functionality allows users to find movies based on various criteria, including title, director, genre, and actors.

### Admin Features
**1. Movie Management:**

Admins can perform CRUD (Create, Read, Update, Delete) operations on movie entries, including adding, editing, and removing movies.

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
2. Go inside the clone folder
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

1. `POST /user/register` for signUp or creating a new user. (The request body should contain the resource data in JSON format.)
```bash
{
   "name": "XYZ",
   "password: 123,
   "role": Admin/User
}
```
2. `POST /user/authenticate` for authentication whether the user exists or is admin or not. (The request body should contain the resource data in JSON format.)
```bash
{
   "name": "XYZ",
   "password: 123,
}
```
3. `POST /movies` Stores a new movie. (The request body should contain the resource data in JSON format.)
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
5. `PUT /movies/<id>` Update an existing movie identified by its ID. (The request body should contain the updated resource data in JSON format.)
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
Note:- The user can provide or update any of the above data to change otherwise it adds the existing data to the table

6. `GET /movies/search/...` Search for existing movies using various filters.

**Getting movies by name**
```bash
http://127.0.0.1:5000/movies/search
{
    "name": ""
}
```

**Getting movies by a director**
```bash
http://127.0.0.1:5000/movies/search?director=XYZ
```

**Getting movies by genre**
```bash
http://127.0.0.1:5000/movies/search?genre=XYZ&genre=ABC
```

**Getting movies by sort**
By default, the movies are sorted by popularity but the user can sort them with imdb_score and id.
```bash
http://127.0.0.1:5000/movies/search?sort_by=id
```

**Getting movies by Order(ascending or descending)**
```bash
http://127.0.0.1:5000/movies/search?order=asc
```
**Note**: The user can combine these filters to generate a customized advanced search query

## Bottlenecks and Solutions
**1. Load Balancing**

Overload can occur in certain conditions like a sudden spike in network traffic, resource exhaustion, and poorly optimized code that exceeds server capacity to handle workload effectively. This leads to performance degradation, reduced responsiveness, and, in extreme cases, system failure. To decrease workload, vertical scaling can be done but there is a limit to it, So, the most relevant solution to this problem is Load Balancing.

through **Load Balancing**, we can distribute incoming network traffic or workloads across multiple servers or resources to ensure efficient resource utilization, high availability, and improved performance. They are typically placed in front of a cluster of servers or resources and continuously monitor the health of servers and route traffic away from failed or unhealthy servers to maintain system reliability.

**2. Complex Queries**

Sometimes database takes a significant amount of time to fetch and return results for queries that involve multiple criteria, joins, or complex calculations. This can happen for various reasons, such as inefficient indexing, large datasets, complex data models, or a lack of optimization. Slow data retrieval can lead to poor application performance and a frustrating user experience. Following are some of the solutions to Speed up data retrieval on complete queries:

**Caching**

Implementing caching mechanisms to store and reuse the results of frequently executed complex queries reduces the load on the database and speeds up data retrieval for subsequent requests. **Redis** may be the solution for this, As **Redis** can be used as a cache for frequently accessed or computationally expensive query results. It stores the results in memory, allowing for lightning-fast retrieval. Complex queries can be executed once, and subsequent requests can be served directly from the Redis cache.

**Database Sharding**

we can horizontally partition a large database into smaller, more manageable pieces called shards. Each shard contains a subset of the data, and together, they make up the complete dataset. It is primarily employed to improve scalability, performance, and availability in large-scale, high-volume applications. There are various ways to shard data, for example, we can data based on genres. we can create separate shards for popular genres like Action, Drama, Comedy, etc. This allows for better distribution of data and optimized queries when users search for movies by genre.

**Indexing**

We can use indexing in a database to improve the speed of data retrieval operations on specific columns or fields. Indexing can significantly enhance query performance. For example, Create an index on the "title" column of the movie database table. This index allows for fast retrieval of movies by their titles.

CREATE INDEX idx_title ON MOVIES(name);

But, it's really important to strike a balance between indexing and database maintenance, as excessive indexing can slow down insert and update operations. So, one needs to regularly monitor and optimize indexes as data grows and access patterns evolve.

