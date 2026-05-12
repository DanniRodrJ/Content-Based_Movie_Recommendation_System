import re
import ast
from fastapi import requests
import numpy as np
import pandas as pd

def get_director(data):
    if isinstance(data, list):
        if len(data) == 0:
            return np.nan
        director_names = [i['name'] for i in data if i['job'] == 'Director']
        if len(director_names) == 0:
            return np.nan
        return ','.join(director_names)
    else:
        return np.nan
    
    
def get_actors(data):
    if isinstance(data, list) == True:
        if len(data) == 0:
            return np.nan
        actors_names = [i['name'] for i in data]
        if len(actors_names) == 0:
            return np.nan
        return ','.join(actors_names)
    else:
        return np.nan
    
    
def contiene_numeros(cadena):
  return bool(re.search(r'\d', str(cadena)))


def stringified(data):
    if isinstance(data, str):
        x = ast.literal_eval(data)
        return x
    else:
        return data
    
    
def get_name(data):
    if isinstance(data, dict):
        name = data['name']
        if name == '':
            return np.nan
        return name
    else:
        return np.nan
    
    
def get_names(data):
    if isinstance(data, list):
        if len(data) == 0:
            return np.nan
        names = [i['name'] for i in data]
        if len(names) == 0:
            return np.nan
        return ','.join(names)
    else:
        return np.nan
    
    
def strip_genres(genres):
  if pd.isnull(genres):
    return genres
  else:
    return genres.replace(' ', '').strip()


def has_duplicates(genres):
  if pd.isnull(genres):
    return False
  else:
    return len(genres.split(',')) != len(set(genres.split(',')))


def lower_case_genres(genres):
  if pd.isnull(genres):
    return genres
  else:
    return genres.lower()


def get_runtime(title, api_key, url_base):
  query = title
  url = f'{url_base}/search/movie'
  params = {'api_key': api_key, 'query': query}
  response = requests.get(url, params=params)
  if response.status_code == 200:
    data = response.json()
    if data['total_results'] > 0:
      movie_id = data['results'][0]['id']
      url = f'{url_base}/movie/{movie_id}'
      params = {'api_key': api_key}
      response = requests.get(url, params=params)
      if response.status_code == 200:
        data = response.json()
        runtime = data['runtime']
        if pd.notnull(runtime):
          return runtime
  return None