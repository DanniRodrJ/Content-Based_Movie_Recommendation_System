# ```Machine Learning Operations (MLOps)```

## ```Introducción```

Como parte de mi formación como Data Scientist en la edtech [Henry](https://www.soyhenry.com/), se me asignó un proyecto para desarrollar un sistema de recomendación de películas. En este proyecto, simulé un ambiente de trabajo real en el cual una start-up de agregación de plataformas de streaming requería un sistema de recomendación que aún no había sido puesto en marcha. Como Data Scientist, mi responsabilidad fue desarrollar el sistema de recomendación de manera integral, desde la recolección y tratamiento de los datos hasta el entrenamiento y despliegue del modelo de Machine Learning. Sin embargo, los datos disponibles en ese momento eran inmaduros y requerían una gran cantidad de trabajo de Data Engineer para transformarlos y prepararlos para su uso en el modelo.

## ✔️```Objetivo```

Desarrollar un sistema de recomendación de películas y series personalizado para una start-up de agregación de plataformas de streaming.

## 💡```Desarrollo del Proyecto```

Para lograr el objetivo, se llevaron a cabo los siguientes procesos:

1. ```Ingeniería de Datos```

    1.1 Extracción, Transformación y Limpieza de los datos (ETL) 👉 [ETL.ipynb]()

    1.2 Disponibilización de los datos limpios

    👉 [api_consultation.csv]()
    👉 [movies_recommendations.csv]()
    👉 [movies_clean.csv]()

    1.3 Desarrollo de la API 👉 [main.py]()

    1.4 Virtualizacion y Deployment para disponibilizar los datos para futuras consultas.

2. ```Machine Learning```

    2.1 Análisis Exploratorio de los datos (EDA) 👉 [EDA.ipynb]()

    2.2 Entrenamiento del Modelo 👉 [ML.ipynb]()

    2.3 Deployment del Modelo de Sistema de Recomendacion de Peliculas 👉 [dannielarodriguez-project-mlops]()

## 🛠️```Tecnologías Utilizadas```

- **Python**: lenguaje de programación principal utilizado en el proyecto.

    ![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)

- **Librerías de Python**: se utilizaron diversas librerías de Python para diferentes tareas en el proyecto como pandas, numpy, datetime, ast, json, requests y re para la limpieza de los datos; fastAPI para las consultas de la data limpia; mientras que para el análisis exploratorio de los datos matplotlib, seaborn y wordcloud; así como scikit-learn para el modelado de sistema de recomendación de películas.

    ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
    ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
    ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
    ![Seaborn](https://img.shields.io/badge/Seaborn-%2370399F.svg?style=for-the-badge&logo=seaborn&logoColor=white)
    ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

- **Google Colab**: plataforma de Jupyter Notebook basada en la nube que se utilizó para el proceso de ETL (Extracción, Transformación y Carga) de los datos, para el EDA (Análisis Exploratorio de datos) y para el Modelo de Machine Learning.

    ![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00.svg?style=for-the-badge&logo=Google-Colab&logoColor=white)

- **Visual Studio Code**: un editor de código fuente desarrollado por Microsoft que se utilizó para escribir y editar el código de Python para el desarrollo de las consultas a la API.
  
    ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=ffffff)

- **Virtualenv**: es una herramienta útil para crear entornos virtuales de Python que permiten instalar y manejar dependencias de forma aislada. Para este caso, se utilizó para gestionar la creación de la API.

    ![venv](https://img.shields.io/badge/Virtualenv-venv-%2300FFFF?style=for-the-badge&logo=python)

- **FastAPI**: un framework de Python para construir APIs web rápidas y escalables.

    ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

- **Render**: servicio en la nube utilizado para implementar el modelo de Machine Learning.

    ![Render](https://img.shields.io/badge/Render-46E3B7.svg?style=for-the-badge&logo=Render&logoColor=white)

## ⚙️ ```ETL```

- La información fue extraída de archivos .csv. La documentación y ubicación respecto a estos archivos se encuentran en la carpeta 📁 [dataset]()
- Fue necesario desanidar la data, ya que existían columnas como ```belongs_to_collection``` , ```production_companies```, ```spoken_languages``` y ```genres``` por mencionar algunos con registros en formato JSON.
- Una vez desanidada la data, se extrajo la información requerida como los nombres de los directores, actores, lenguajes hablados, etc. Los cuales fueron añadidos al Dataframe para facilitar consultas posteriores.
- Se eliminaron las columnas que no se iban a utilizar, como ```video```, ```imdb_id```, ```adult```,```original_title```, ```poster_path``` y ```homepage```.
- Se creo una nueva columna llamada ```return``` para permitir consultas relacionadas al retorno de inversión por película y director.
- Se utilizó la API de TMDB para impitar datos faltantes en columnas que podían ser claves para el sistema de recomendación de películas como ```genre```.
- Se emplearon técnicas como WordNetLemmatizer y word_tokenize para limpiar los caracteres especiales en columnas como ```overview```, evitando la pérdida de posibles palabras importantes para el sistema de recomendación.
- Finalmente, se realizaron las siguientes importaciones:
  - Toda la data limpia a un archivo .csv llamado 👉 [movies_clean]()
  - Data limpia con sólo las columnas necesarias para las consultas 👉 [api_consultations.csv]()

## 🖥️```FastAPI```

Se propone el desarrollo de una API para disponibilizar los datos de la empresa a través del framework FastAPI. Presentando 6 endpoints, en el archivo 👉 [main.py]() que se consumirán en la API. 

Primero se construyó la API de forma local y se configuraron las funciones necesarias para realizar las consultas, cargando la data desde el archivo 👉 [api_consultations.csv]() que se disponibilizó a través del ETL.

Estos endpoints son los siguientes:

- ```def cantidad_filmaciones_mes(Mes)```: Consulta que devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset

        Formato de salida: {'mes': mes, 'cantidad': cantidad}

- ```def cantidad_filmaciones_dia(Dia)```: Consulta que devuelve la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset

        Formato de salida: {'dia': dia, 'cantidad': cantidad}

- ```def score_titulo(titulo_de_la_filmación)```: Consulta que devuelve el título, el año de estreno y el score de una filmación

        Formato de salida: {'titulo': titulo, 'anio': year, 'popularidad': score}

- ```def votos_titulo(titulo_de_la_filmación)```: Consulta que devuelve título, la cantidad de votos y el valor promedio de las votaciones de una filmación siempre y cuando supere las 2000 valoraciones.

        Formato de salida: {'titulo': titulo, 'año': year, 'voto_total': voto_total, 'voto_promedio': voto_promedio}

- ```def get_actor(nombre_actor)```: Consulta que devuelve el éxito de un actor medido a través del retorno de inversión, así como la cantidad de películas que en las que ha participado y el promedio de retorno.

        Formato de salida: {'actor': nombre_actor, 'cantidad_filmaciones': cantidad_peliculas, 'retorno_total': retorno_total, 'retorno_promedio': retorno_promedio}

- ```def get_director(nombre_director)```: Consulta que devuelve el éxito de un director medido a través del retorno de inversión, nombre de cada película que ha dirigido con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

        Formato de salida: {'director': nombre_director,
            'retorno_total_director': retorno_total_director,
            'peliculas': [{
            'titulo': row['title'],
            'anio': row['release_year'],
            'retorno_pelicula': round(row['return'], 4),
            'budget_pelicula': row['budget'],
            'revenue_pelicula': row['revenue']
        }],
            }

Estos endpoints permitirán que los empleados de la empresa puedan hacer solicitudes específicas a la API para obtener información valiosa o realizar acciones específicas.

## 📊 ```EDA```

Una vez que los datos fueron limpiados, se realizó una análisis exploratorio para identificar patrones, relaciones y tendencias en los datos, así como valores atípicos. En este contexto se llevaron a cabo algunas exploraciones interesantes en las siguientes columnas:

- La nube de palabras de las columnas genre, title y overview proporcionó información útil permitiendo identificar los géneros más populares así como las palabras más comunes en los títulos en las descripciones de las películas.
- Se utilizó un histograma de distribución de la longitud tanto para los títulos como para las descripciones, concluyendo que la mayoría de los títulos son relativamente cortos mientras que para el caso de la columna overview se identificó dos grupos diferentes de resúmenes con diferentes longitudes.
- Mientras que las columnas como popularity, revenue presentaron una distribución fuertemente sesgada debido a valores atípicos. Como por ejemplo películas que han generado una gran cantidad de ingresos en taquilla y que por otro lado están las que no lograron recaudar o el valor de su ingreso aún no ha sido registrado.
- Hay variables que presentaron una fuerte relación positiva como son el caso de revenue y vote_count con 0.81, así como revenue y budget.
- Por otro lado, se observaron datos interesantes como que John Ford es el director con más número de apariciones, los resúmenes más cortos presentaron una mejor calificación promedio, el viernes es el día predilecto para el lanzamiento de las películas, etc. 

## 🤖```Machine Learning```

Para implementar el sistema de recomendación, se utilizó la librería scikit-learn de Python, y se aplicó la técnica de vectorización TF-IDF para crear una matriz de vectores que describía el contenido de las películas en función de sus sinopsis. Luego, se utilizó la medida de similitud del coseno para calcular la similitud entre cada par de películas, y se ordenaron las películas según su score de similaridad.

El resultado final fue una función de recomendación de películas escrita en Python, que toma como entrada el título de una película y devuelve una lista de las 5 películas más similares, ordenadas según su score de similaridad. La función también maneja casos en los que el título de la película no se encuentra en la base de datos o cuando hay títulos de películas duplicados que fueron lanzados en años distintos.

Finalmente fue deployado como una función adicional de la API, llamada:

- ```def recomendacion(titulo)```: Se ingresa el nombre de una película y recomienda las similares en una lista de 5 valores.

        Formato de salida: ['titulo_recomendado1', 'titulo_recomendado2', 'titulo_recomendado3', 'titulo_recomendado4', 'titulo_recomendado5']

## ```Render```

Para hacer el despliegue de las funciones de la API que incluyen las consultas así como el sistema de recomendación de películas se utilizó Render. El cual permitirá al equipo de la start-up poder realizar las consultas a través de una página web 👉 [render]()

## 📋```Video y recomendaciones```



## 👩‍💻 ```Desarrollador```

![linkedin](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)