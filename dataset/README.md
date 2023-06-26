# Fuente de Datos

## Archivos sin procesar

Los archivos (```credits.csv``` y ```movies_dataset.csv```) se encuentran alojados en Google Drive, por lo que puedes acceder a ellos mediante el siguiente [link](https://drive.google.com/drive/folders/1uYpitLzf2ZTTltMB8LuqmZY8ctHLLIaV?usp=sharing)

## Data limpia

El archivo csv limpio obtenido del proceso ETL realizado en el notebook ETL_Movies.ipynb se encuentra alojado en este repositorio con el nombre de ```movies_clean.csv```

## Data para el modelo de Machine Learning

## Diccionario de datos

El archivo ```credits.csv``` contiene las siguientes características:

* **id** - Un identificador único para cada película.
* **cast** - El nombre de los actores principales y secundarios.
* **crew** - Nombre del director, editor, compositor, guionista, etc.

El archivo ```movies_dataset.csv``` contiene las siguientes características:

* **adult** - Indica si la película tiene calificación X, exclusiva para adultos.
* **belongs_to_collection** - Un diccionario que indica a que franquicia o serie de películas pertenece la película.
* **budget** - El presupuesto de la película en dólares.
* **genres** - Un diccionario que indica todos los géneros asociados a la película.
* **homepage** - La pagina web oficial de la película.
* **id** - ID de la película.
* **imdb_id** - IMDB ID de la película.
* **original_language** - Idioma original en el que se grabó la película.
* **original_title** - Titulo original de la película.
* **overview** - Resumen de la película.
* **popularity** - Puntaje de popularidad de la película, asignado por TMDB (TheMoviesData).
* **poster_path** - URL del poster de la película.
* **production_companies** - Lista de compañías productoras asociadas a la película.
* **production_countries** - Lista con los países donde se produjo la película.
* **release_date** - Fecha de estreno de la película.
* **revenue** - Recaudación de la película, en dólares.
* **runtime** - Duración de la película, en minutos.
* **spoken_languages** - Lista con los idiomas que se hablan en la película.
* **status** - Estado actual de la película (si fue anunciada, si ya se estrenó, etc).
* **tagline** - Frase celebre asociada a la película
* **title** - Título de la película.
* **vote_average** - Puntaje promedio de reseñas de la película.
* **vote_count** - Número de votos recibidos por la película, en TMDB.
