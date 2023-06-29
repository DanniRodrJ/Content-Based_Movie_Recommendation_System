# Machine Learning Operations (MLOps)

## Introducción

Como parte de mi formación como Data Scientist en la edtech [Henry](https://www.soyhenry.com/), se me asignó un proyecto para desarrollar un sistema de recomendación de películas. En este proyecto, simulé un ambiente de trabajo real en el cual una start-up de agregación de plataformas de streaming requería un sistema de recomendación para mejorar la experiencia del usuario y aumentar la retención de clientes. Como Data Scientist, mi responsabilidad fue desarrollar el sistema de recomendación de manera integral, desde la recolección y tratamiento de datos hasta el entrenamiento y mantenimiento del modelo de Machine Learning. Sin embargo, los datos disponibles en ese momento eran inmaduros y requerían una gran cantidad de trabajo de Data Engineer para transformarlos y prepararlos para su uso en el modelo.

## Objetivo

El objetivo de este proyecto era desarrollar un sistema de recomendación de películas y series personalizado para una start-up de agregación de plataformas de streaming, utilizando técnicas de Machine Learning. El sistema de recomendación se basó en el análisis de la similitud textual entre las sinopsis de las películas, utilizando la técnica de vectorización TF-IDF. El proyecto abarcó todo el ciclo de vida de un proyecto de Machine Learning, desde la recolección y tratamiento de datos hasta el entrenamiento y mantenimiento del modelo de Machine Learning.

## Desarrollo del Proyecto

## Tecnologías Utilizadas

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

- **Virtualenv**:

    ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

- **FastAPI**: un framework de Python para construir APIs web rápidas y escalables.

    ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

- **Render**: servicio en la nube utilizado para implementar el modelo de Machine Learning.

    ![Render](https://img.shields.io/badge/Render-46E3B7.svg?style=for-the-badge&logo=Render&logoColor=white)

## ETL

## FastAPI

## Machine Learning

Para implementar el sistema de recomendación, se utilizó la librería scikit-learn de Python, y se aplicó la técnica de vectorización TF-IDF para crear una matriz de vectores que describía el contenido de las películas en función de sus sinopsis. Luego, se utilizó la medida de similitud del coseno para calcular la similitud entre cada par de películas, y se ordenaron las películas según su score de similaridad.

El resultado final fue una función de recomendación de películas escrita en Python, que toma como entrada el título de una película y devuelve una lista de las 5 películas más similares, ordenadas según su score de similaridad. La función también maneja casos en los que el título de la película no se encuentra en la base de datos o cuando hay títulos de películas duplicados que fueron lanzados en años distintos.

## Recomendaciones

## Desarrollador

