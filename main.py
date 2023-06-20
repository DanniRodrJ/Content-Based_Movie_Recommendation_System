from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_csv("Dataset/movies_clean.csv", parse_dates = ["release_date"])

@app.get("/")
async def index():
    return "Hola! API realizada por Danniela Rodríguez"

@app.get("/about")
async def about():
    return "Proyecto MLOps"

# Consigna 1
@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    '''Se ingresa el mes y la función retorna la cantidad de películas que se estrenaron ese mes históricamente'''
    # Convertir el mes a minúsculas para facilitar la comparación
    mes = mes.lower()
    # Diccionario para mapear los nombres de los meses en español con sus equivalentes en inglés
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
    # Devolver la respuesta como un diccionario
    return {'mes': mes, 'cantidad': cantidad}


# Consigna 2 
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa el dia y la función retorna la cantidad de películas que se estrenaron ese dia históricamente'''
    # Convertir el día a minúsculas para facilitar la comparación
    dia = dia.lower()
    # Crear un diccionario para mapear los nombres de los días en español con sus equivalentes en inglés
    dias = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
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
    # Devolver la respuesta como un diccionario
    return {'dia': dia, 'cantidad': cantidad}


# Consigna 3
@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    # Filtrar el dataframe por el título de la película
    resultado = df[df["title"] == titulo]
    # Verificar si el resultado está vacío
    if resultado.empty:
        return f"No se encontró la película {titulo}"
    else:
        # Obtener el título, año de estreno y score/popularidad
        title = resultado["title"].iloc[0]
        year = resultado["release_year"].iloc[0]
        score = resultado["popularity"].iloc[0]
        # return f"La película {title} fue estrenada en el año {year} con un score/popularidad de {round(score, 4)}"
        return {'titulo': title, 'anio': year, 'popularidad': score}


# Consigna 4:
@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor 
    promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, 
    retornara un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningún 
    valor.'''
    # Filtrar el dataframe por el título de la filmación
    resultado = df[df["title"] == titulo]
    # Verificar si el resultado está vacío
    if resultado.empty:
        return f"No se encontró la filmación {titulo}"
    else:
        # Obtener el año de estreno, votos totales y promedio de votos
        year = resultado["release_year"].iloc[0]
        voto_total = resultado["vote_count"].iloc[0]
        voto_promedio = resultado["vote_average"].iloc[0]
    # Verificar si la cantidad de votos es mayor o igual a 2000
    if voto_total >= 2000:
        return {'titulo': titulo, 'año': year, 'voto_total': voto_total, 'voto_promedio': voto_promedio}
    else:
        return f"No se encontraron suficientes votos para la filmación {titulo}"


# Consigna 5:
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset y la función retorna el éxito del 
    mismo medido a través del retorno, la cantidad de películas que en las que ha participado y el promedio de 
    retorno.'''
    # Copia del dataframe original
    df_copy = df.copy()
    # Reemplazar los valores NaN en la columna "actors" con una cadena vacía ""
    df_copy["actors"].fillna("", inplace=True)
    # Separar los nombres de los actores en una lista
    df_copy["actors_list"] = df_copy["actors"].str.split(",")
    # Función lambda para filtrar el dataframe por el nombre del actor
    df_filtrado = df_copy[df_copy["actors_list"].apply(lambda x: nombre_actor in x)]
    # Cantidad de películas en las que el actor ha participado
    cantidad_peliculas = len(df_filtrado)
    # Calcular el retorno promedio de las películas en las que el actor ha participado
    retorno_promedio = df_filtrado["return"].mean()
    # Calcular el retorno total del actor en todas las películas en las que ha participado
    retorno_total = df_filtrado["return"].sum()
    # return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} filmaciones, el mismo ha conseguido un retorno de {round(retorno_total, 4)} con un promedio de {round(retorno_promedio, 4)} por filmación"
    return {'actor': nombre_actor, 'cantidad_filmaciones': cantidad_peliculas, 'retorno_total': retorno_total, 'retorno_promedio': retorno_promedio}


# Consigna 6
