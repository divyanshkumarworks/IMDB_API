import json 
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

with open('imdb.json','r') as json_File :
	sample_load_file=json.load(json_File)

	# for adding data to Director table
	i = 1
	for item in sample_load_file:
		cursor.execute("SELECT * FROM Director WHERE name = ?", (item['director'],))
		matching_directors = cursor.fetchall()
		if matching_directors:
			continue
		else:
			cursor.execute("INSERT INTO Director (id, name) VALUES (?, ?)", (i, item['director']))
			i += 1

	# for adding data to IMDB_SCORE table
	i = 1
	for item in sample_load_file:
		cursor.execute("SELECT * FROM IMDB_SCORE WHERE score = ?", (item['imdb_score'],))
		matching_score = cursor.fetchall()
		if matching_score:
			continue
		else:
			cursor.execute("INSERT INTO IMDB_SCORE (id, score) VALUES (?, ?)", (i, item['imdb_score']))
			i += 1

	# for adding data to POPULARITY table
	i = 1
	for item in sample_load_file:
		cursor.execute("SELECT * FROM POPULARITY WHERE popularity = ?", (item['99popularity'],))
		matching_popularity = cursor.fetchall()
		if matching_popularity:
			continue
		else:
			cursor.execute("INSERT INTO POPULARITY (id, popularity) VALUES (?, ?)", (i, item['99popularity']))		
			i += 1

	
	# for adding data to GENRE table
	i = 1
	for item in sample_load_file:
		for word in item['genre']:
			cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + word + "%",))
			matching_genre = cursor.fetchall()
			if matching_genre:
				continue
			else:
				cursor.execute("INSERT INTO GENRE (id, genre) VALUES (?, ?)", (i, word))		
				i += 1

	for adding data to MOVIES table
	
	for item in sample_load_file:
		cursor.execute("SELECT * FROM Director WHERE name = ?", (item['director'],))
		matching_directors = cursor.fetchall()

		cursor.execute("SELECT * FROM IMDB_SCORE WHERE score = ?", (item['imdb_score'],))
		matching_score = cursor.fetchall()

		cursor.execute("SELECT * FROM POPULARITY WHERE popularity = ?", (item['99popularity'],))
		matching_popularity = cursor.fetchall()
	
		cursor.execute("INSERT INTO movies (name, imdb_score, director, popularity) VALUES (?, ?, ?, ?)", (item['name'], matching_score[0][0], matching_directors[0][0], matching_popularity[0][0]))

	for adding data to MOVIE_GENRE table
	i = 1
	for item in sample_load_file:
		for word in item['genre']: 
			cursor.execute("SELECT * FROM GENRE WHERE genre LIKE ?", ("%" + word + "%",))
			matching_genre = cursor.fetchall()
			if matching_genre:
				cursor.execute("INSERT INTO MOVIES_GENRE (genre_id, movie_id) VALUES (?, ?)", (matching_genre[0][0], i))
		i += 1

connection.commit()
connection.close()