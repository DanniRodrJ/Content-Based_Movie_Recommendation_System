# Importación de librerías necesarias
from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Punto de partida para construir una aplicación web API
app = FastAPI()

# Leer los archivos .csv para el consumo de la API
df = pd.read_csv("api_consultations.csv", parse_dates = ["release_date"])
df2 = pd.read_csv("movies_recommendations.csv")

# Ruta de inicio
@app.get("/")
async def index():
    message = "¡Bienvenid@ a mi API para consultar y recibir recomendaciones de películas! Para más información, visite /docs"
    return {"message": message}

# Ruta de información
@app.get("/about")
async def about():
    return "Esta es una aplicación FastAPI creada por Danniela Rodríguez Jove, en junio de 2023."


# Ruta de cantidad de filmaciones para un determinado mes 
@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    '''Se ingresa el mes y la función retorna la cantidad de películas que se estrenaron ese mes históricamente.'''
    # Convertir el mes a minúsculas para facilitar la comparación
    mes = mes.lower()
    # Se crea un diccionario para mapear los nombres de los meses en español con sus equivalentes en inglés
    meses = {
        'enero': 'January',
        'febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December'
    }
    # Verificar si el mes ingresado es válido
    if mes not in meses:
        return f"El mes {mes} no es válido"
    # Obtener el nombre del mes en inglés
    mes_ingles = meses[mes]
    # Filtrar el dataframe por el mes de estreno
    resultado = df[df["release_date"].dt.strftime('%B') == mes_ingles]
    # Obtener la cantidad de películas estrenadas en el mes
    cantidad = len(resultado)
    # Se devuelve la respuesta como un diccionario
    return {'mes': mes, 'cantidad': cantidad}


# Ruta de cantidad de filmaciones para un determinado día de la semana 
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa el dia y la función retorna la cantidad de películas que se estrenaron ese dia históricamente.'''
    # Convertir el día a minúsculas para facilitar la comparación
    dia = dia.lower()
    # Se crea un diccionario para mapear los nombres de los días en español con sus equivalentes en inglés
    dias = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }
    # Verificar si el día ingresado es válido
    if dia not in dias:
        return f"El día {dia} no es válido"
    # Obtener el nombre del día en inglés
    dia_ingles = dias[dia]
    # Filtrar el dataframe por el día de la semana de estreno
    resultado = df[df["release_date"].dt.strftime('%A') == dia_ingles]
    # Obtener la cantidad de películas estrenadas en el día
    cantidad = len(resultado)
    # Se devuelve la respuesta como un diccionario
    return {'dia': dia, 'cantidad': cantidad}


# Ruta de búsqueda por título
@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.'''
    # Copia del dataframe original para no afectar futuras consultas 
    df_copy = df.copy()
    # Crear una copia de la columna de title en minúsculas
    df_copy["title_lower"] = df_copy["title"].str.lower()
    # Convertir el título a minúsculas y capitalizar la primera letra
    titulo_lower = titulo.lower()
    # Filtrar el dataframe por el título de la filmación
    resultado = df_copy[df_copy["title_lower"] == titulo_lower]
    # Verificar si el resultado está vacío
    if resultado.empty:
        return f"No se encontró la filmación {titulo}"
    else:
        # Obtener la fila con la popularidad más alta para el título dado
        fila_max_pop = resultado.loc[resultado['popularity'].idxmax()]
        # Obtener el título, año de estreno y score/popularidad de la fila con la popularidad más alta
        titulo = fila_max_pop["title"]
        year = int(fila_max_pop["release_year"])
        score = fila_max_pop["popularity"]
        # Se devuelve la respuesta como un diccionario
        return {'titulo': titulo, 'anio': year, 'popularidad': score}


# # Ruta de cantidad de votos para una determina película
@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor 
    promedio de las votaciones. La misma película deberá de contar con al menos 2000 valoraciones, caso contrario, 
    se retorna un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningún 
    valor.'''
    # Copia del dataframe original para no afectar futuras consultas 
    df_copy = df.copy()
    # Crear una copia de la columna de title en minúsculas
    df_copy["title_lower"] = df_copy["title"].str.lower()
    # Convertir el título a minúsculas y capitalizar la primera letra
    titulo_lower = titulo.lower()
    # Filtrar el dataframe por el título de la filmación
    resultado = df_copy[df_copy["title_lower"] == titulo_lower]
    # Verificar si el resultado está vacío
    if resultado.empty:
        return f"No se encontró la filmación {titulo}"
    else:
        # Obtener el año de estreno, votos totales y promedio de votos
        year = int(resultado["release_year"].iloc[0])
        voto_total = int(resultado["vote_count"].iloc[0])
        voto_promedio = resultado["vote_average"].iloc[0]
        # Retornar el nombre del titulo ubicado en la columna title
        titulo = resultado["title"].iloc[0]
        # Verificar si la cantidad de votos es mayor o igual a 2000
        if voto_total >= 2000:
            # Se devuelve la respuesta como un diccionario
            return {'titulo': titulo, 'año': year, 'voto_total': voto_total, 'voto_promedio': voto_promedio}
        else:
            # En caso de que la cantidad de votos sea inferior a 2000, se devuelve un mensaje
            return f"No se encontraron suficientes votos para la filmación {titulo}"


# Ruta de búsqueda por actor
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    '''Se ingresa el nombre de un actor que se encuentre dentro del dataset y la función retorna: el éxito del 
    mismo medido a través del retorno, la cantidad de películas que en las que ha participado y el promedio de 
    retorno.'''
    # Copia del dataframe original para no afectar futuras consultas 
    df_copy = df.copy()
    # Reemplazar los valores NaN en la columna "actors" con una cadena vacía ""
    df_copy["actors"].fillna("", inplace=True)
    # Separar los nombres de los actores en una lista
    df_copy["actors_list"] = df_copy["actors"].str.split(",")
    # Convertir el nombre del director a minúsculas
    nombre_actor = nombre_actor.title()
    # Función lambda para filtrar el dataframe por el nombre del actor
    df_filtrado = df_copy[df_copy["actors_list"].apply(lambda x: nombre_actor in [nombre.title() for nombre in x])]
    # Cantidad de películas en las que el actor ha participado
    cantidad_peliculas = len(df_filtrado)
    # Calcular el retorno promedio de las películas en las que el actor ha participado
    retorno_promedio = round(df_filtrado["return"].mean(), 4)
    # Calcular el retorno total del actor en todas las películas en las que ha participado
    retorno_total = round(df_filtrado["return"].sum(), 4)
    return {'actor': nombre_actor, 'cantidad_filmaciones': cantidad_peliculas, 'retorno_total': retorno_total, 'retorno_promedio': retorno_promedio}


# Ruta de búsqueda por director
@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    '''Se ingresa el nombre de un director que se encuentre dentro del dataset debiendo devolver: el éxito del
    mismo a través del retorno, el nombre de cada película que ha dirigido con la fecha de lanzamiento,
    retorno individual, costo y ganancia de la misma.'''
    # Copia del dataframe original para no afectar futuras consultas 
    df_copy = df.copy()
    # Reemplazar los valores NaN en la columna "director" por una cadena vacía ""
    df_copy["director"].fillna("", inplace=True)
    # Separar los nombres de los directores en una lista
    df_copy["director_list"] = df_copy["director"].str.split(",")
    # Convertir el nombre del director a minúsculas
    nombre_director = nombre_director.title()
    # Función lambda para filtrar el dataframe por el nombre del director
    resultado = df_copy.loc[df_copy["director_list"].apply(lambda x: nombre_director in [nombre.title() for nombre in x])]
    # Verificar si el resultado está vacío
    if resultado.empty:
        return f"No se encontró el director {nombre_director}"
    # Obtener el retorno total del director
    retorno_total_director = round(resultado["return"].sum(), 4)
    # Se crea una lista de diccionarios con la información de cada película que dirigió el director
    peliculas = []
    for index, row in resultado.iterrows():
        pelicula = {
            'titulo': row['title'],
            'anio': row['release_year'],
            'retorno_pelicula': round(row['return'], 4),
            'budget_pelicula': row['budget'],
            'revenue_pelicula': row['revenue']
        }
        peliculas.append(pelicula)
    # Se devuelve la respuesta como un diccionario
    return {'director': nombre_director,
            'retorno_total_director': retorno_total_director,
            'peliculas': peliculas,
            }


# Machine Learning
'''Dado que el entorno gratuito de Render presenta limitaciones de memoria RAM, estratégicamente 
se coloca la creación del objeto TfidfVectorizer fuera de la función recomendacion(). De esta manera se 
garantiza que tfidf, y tfidf_matriz sean variables globales que se ejecutaran idealmente una sola vez 
(cuando se carga el módulo), independientemente de cuántas veces se llame a la función recomendacion().'''
# Se crea una instancia de la clase TfidfVectorizer con los parámetros deseados
tfidf_1 = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
# Aplicar la transformación TF-IDF al texto contenido en la columna "overview" de 'df2'
tfidf_matriz_1 = tfidf_1.fit_transform(df2['overview'])

# Ruta de recomendación de peliculas
@app.get('/recomendacion/{titulo}')
async def recomendacion(titulo: str):
    '''Se ingresa el nombre de una película y se recomienda las 5 películas más similares en una lista'''
    # Se crea un objeto 'indices' que mapea los títulos de las películas a sus índices correspondientes en el DataFrame 'df2'
    indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()
    # Se busca el índice de la película de entrada utilizando el objeto 'indices'
    idx = pd.Series(indices[titulo]) if titulo in indices else None
    # Si la película de entrada no se encuentra en el DataFrame, se devuelve un mensaje de error
    if idx is None:
        return "Película no encontrada"
    # Si el título de la película está duplicado, se devuelve el índice de la primera aparición del título en el DataFrame
    if df2.duplicated(['title']).any():
        primer_idx = df2[df2['title'] == titulo].index[0]
        if not idx.equals(pd.Series(primer_idx)):
            idx = pd.Series(primer_idx)
    # Se calcula la similitud coseno entre la película de entrada y todas las demás películas en la matriz de características
    similitud = sorted(enumerate(cosine_similarity(tfidf_matriz_1[idx], tfidf_matriz_1).flatten()), key=lambda x: x[1], reverse=True)[1:6]
    # Se obtienen los títulos de las películas más similares utilizando el índice de cada película
    recomendaciones = df2.iloc[[i[0] for i in similitud], :]['title'].tolist()
    # Se devuelve la lista de títulos de las películas recomendadas
    return {'lista recomendada': recomendaciones}
    