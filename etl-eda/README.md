# ETL - EDA

## ⚙️ ```ETL```

![etl](/assets/ETL.png)

- La información fue extraída de archivos ```.CSV```. La documentación y ubicación respecto a estos archivos se encuentran en la 📁[dataset](https://github.com/DanniRodrJ/Project_MLOps/tree/main/dataset)
- Fue necesario desanidar la data, ya que existían columnas como ```belongs_to_collection``` , ```production_companies```, ```spoken_languages``` y ```genres``` por mencionar algunos con registros en formato JSON.
- Una vez desanidada la data, se extrajo la información requerida como los nombres de los directores, actores, lenguajes hablados, etc. Los cuales fueron añadidos al Dataframe para facilitar consultas posteriores.
- Se eliminaron las columnas que no se iban a utilizar, como ```video```, ```imdb_id```, ```adult```,```original_title```, ```poster_path``` y ```homepage```.
- Se creó una nueva columna llamada ```return``` para permitir consultas relacionadas al retorno de inversión por película y director.
- Se utilizó la **API de TMDB** para imputar datos faltantes en columnas que podían ser claves para el sistema de recomendación de películas como ```genre```.
- Se emplearon técnicas como **WordNetLemmatizer** y **word_tokenize** para limpiar los caracteres especiales en columnas como ```overview```, evitando la pérdida de posibles palabras importantes para el sistema de recomendación.
- Para dejar todas las descripciones de la columna ```overview``` en un único idioma (inglés), se empleó la librería de **googletrans** que implementa la API de Google Translate.
- Finalmente, se realizaron las siguientes exportaciones:
  - Toda la data limpia a un archivo .parquet llamado 👉 [movies_clean.parquet](https://github.com/DanniRodrJ/Project_MLOps/blob/main/dataset/movies_clean.parquet)
  - Data limpia con sólo las columnas necesarias para las consultas 👉 [api_consultation.parquet](https://github.com/DanniRodrJ/Project_MLOps/blob/main/api_consultations.parquet)

## 📊 ```EDA```

![EDA](/assets/EDA.png)

Una vez que los datos fueron limpiados, se realizó un análisis exploratorio para identificar patrones, relaciones y tendencias en los datos, así como valores atípicos. En este contexto se llevaron a cabo algunas exploraciones interesantes en las siguientes columnas:

- La nube de palabras de las columnas ```genre```, ``title`` y ```overview``` proporcionó información útil permitiendo identificar los géneros más populares así como las palabras más comunes en los títulos de las descripciones de las películas.

  ```title```
  ![title](/assets/title.png)
  ```overview```
  ![overview](/assets/overview.png)

- Se utilizó un histograma de distribución de la longitud tanto para los títulos como para las descripciones, concluyendo que la mayoría de los títulos son relativamente cortos mientras que para el caso de la columna ```overview``` se identificó dos grupos diferentes de resúmenes con diferentes longitudes.

  ![long_title](/assets/longitud_title.png)
- Algunas columnas como ```popularity``` y ```revenue```, presentaron una distribución fuertemente sesgada debido a la presencia de valores atípicos. Por ejemplo, algunas películas han generado una gran cantidad de ingresos en taquilla, mientras que otras no lograron recaudar o el valor de sus ingresos aún no ha sido registrado. Destacando que estos valores atípicos no eran necesariamente errores en los datos.
- Hay variables que presentaron correlaciones positivas significativas, indicando que:

  ![correlacion](/assets/corr.png)
  - Las películas con mayores presupuestos tienden a generar mayores ingresos (0.77) y recibir mas votos (0.68)
  - Las películas que generan mayores ingresos también suelen recibir más votos de los espectadores (0.81).
  - Las películas populares tienen una tendencia moderada a recibir más votos (0.56) y generar mayores ingresos (0.51).
- Por otro lado, se observaron datos interesantes como que:
  - John Ford es el director con más número de apariciones.
  - Las descripciones más cortas presentaron una mejor calificación promedio.
  - El viernes es el día predilecto para el lanzamiento de las películas.

![dia](/assets/dia.png)