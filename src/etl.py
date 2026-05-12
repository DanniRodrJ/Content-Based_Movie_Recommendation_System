import ast
import os
import re
from fastapi import requests
import numpy as np
import pandas as pd
import utils as ut

movies_csv = pd.read_csv('../data/movies_dataset.csv', low_memory=False) 
credits_csv = pd.read_csv('../data/credits.csv', low_memory=False)

# Credits
columns_credits = ['cast', 'crew']
for atribute in columns_credits:
    credits_csv[atribute] = credits_csv[atribute].apply(lambda x: ast.literal_eval(str(x)))
    
credits_csv['director'] = credits_csv['crew'].apply(lambda x: ut.get_director(x))
credits_csv['actors'] = credits_csv['cast'].apply(lambda x: ut.get_actors(x))    

credits = credits_csv[['id', 'director', 'actors']].copy()
duplicate_credits = credits[credits.duplicated(subset = 'id', keep = False)]
if duplicate_credits.shape[0]:
    credits.drop_duplicates(subset = 'id', inplace = True)

# Movies
columns_drop = ['adult', 'imdb_id', 'homepage', 'original_title', 'poster_path', 'video']
movies_csv.drop(columns_drop, axis = 1, inplace = True)
movies_csv['original_language'] = movies_csv['original_language'].astype(str)
condicion = movies_csv['original_language'].apply(ut.contiene_numeros)
movies_csv.loc[condicion, 'original_language'] = np.nan
movies_csv.loc[movies_csv['overview'].str.strip() == '', 'overview'] = np.nan
movies_csv['tagline'] = movies_csv['tagline'].replace('-', np.nan)

copy_movies = movies_csv.copy()

columns_movies = ['belongs_to_collection', 'genres', 'production_companies', 'production_countries', 'spoken_languages']
for columns in columns_movies:
    copy_movies[columns] = copy_movies[columns].apply(lambda x: ut.stringified(x))
copy_movies['collection'] = copy_movies['belongs_to_collection'].apply(lambda x: ut.get_name(x))

columns_movies_1 = ['genres', 'production_companies', 'production_countries']
for atribute in columns_movies_1:
    copy_movies[atribute] = copy_movies[atribute].apply(lambda x: ut.get_names(x))
copy_movies['languages'] = copy_movies['spoken_languages'].apply(lambda x: ut.get_names(x))

copy_movies.loc[copy_movies['languages'].str.strip() == '', 'languages'] = np.nan
copy_movies.drop(index = [19730, 29503, 35587], inplace = True)

copy_movies['id'] = copy_movies['id'].astype('int32', errors = 'raise')
copy_movies['budget'] = copy_movies['budget'].astype('int32', errors = 'raise')
copy_movies['popularity'] = copy_movies['popularity'].astype('float64', errors = 'raise')
copy_movies['release_date'] = pd.to_datetime(copy_movies['release_date'], format = '%Y-%m-%d')

# Movies Duplicates
movies = copy_movies[['budget', 'genres',	'id',	'original_language', 'overview',
    'popularity', 'production_companies', 'production_countries',	'release_date',
    'revenue', 'runtime', 'status', 'tagline', 'title',	'vote_average',
    'vote_count',	'collection',	'languages']].copy()

id_duplicated = [141971, 5511, 168538, 18440, 265189, 11115, 42495, 152795, 298721, 25541, 105045, 119916, 159849, 23305, 97995, 99080]

for i in id_duplicated:
  index = movies[movies['id'] == i].index.tolist()
  if len(index) == 3:
    drop_index = index[-2:]
    movies.drop(labels = drop_index, inplace = True)
  else:
    drop_index = index[-1]
    movies.drop(labels = drop_index, inplace = True)
    
# Duplicates with different values in one or two columns    
sustitucion_132641 = movies[movies['id'] == 132641][['id','popularity']]
new_value = round(sustitucion_132641.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 838
drop_index = 30001
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_10991 = movies[movies['id'] == 10991][['id','popularity','vote_count']]
new_value = round(sustitucion_10991.groupby('id')['popularity'].median().iloc[0], 6)
new_value_1 = round(sustitucion_10991.groupby('id')['vote_count'].median().iloc[0], 1)
row_index = 4114
drop_index = 44821
movies.loc[row_index, 'popularity'] = new_value
movies.loc[row_index, 'vote_count'] = new_value_1
movies.drop(labels = drop_index, inplace = True)

sustitucion_4912 = movies[movies['id'] == 4912][['id','popularity']]
new_value = round(sustitucion_4912.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 5865
drop_index = 33826
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_15028 = movies[movies['id'] == 15028][['id','popularity', 'vote_count']]
new_value = round(sustitucion_15028.groupby('id')['popularity'].median().iloc[0], 6)
new_value_1 = round(sustitucion_15028.groupby('id')['vote_count'].median().iloc[0], 1)
row_index = 5130
drop_index = 33743
movies.loc[row_index, 'popularity'] = new_value
movies.loc[row_index, 'vote_count'] = new_value_1
movies.drop(labels = drop_index, inplace = True)

sustitucion_14788 = movies[movies['id'] == 14788][['id','popularity']]
new_value = round(sustitucion_14788.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 10419
drop_index = 12066
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_84198 = movies[movies['id'] == 84198][['id','popularity']]
new_value = round(sustitucion_84198.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 2564
drop_index = 21116
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_13209 = movies[movies['id'] == 13209][['id','popularity']]
new_value = round(sustitucion_13209.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 11342
drop_index = 15765
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_77221 = movies[movies['id'] == 77221][['id','popularity']]
new_value = round(sustitucion_77221.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 11155
drop_index = 20843
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_109962 = movies[movies['id'] == 109962][['id','popularity']]
new_value = round(sustitucion_109962.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 5710
drop_index = 20899
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_22649 = movies[movies['id'] == 22649][['id','popularity']]
new_value = round(sustitucion_22649.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 949
drop_index = 15074
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_110428 = movies[movies['id'] == 110428][['id','popularity']]
new_value = round(sustitucion_110428.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 4356
drop_index = 23534
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_69234 = movies[movies['id'] == 69234][['id','popularity']]
new_value = round(sustitucion_69234.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 9576
drop_index = 26625
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

sustitucion_12600 = movies[movies['id'] == 12600][['id','popularity']]
new_value = round(sustitucion_12600.groupby('id')['popularity'].median().iloc[0], 6)
row_index = 5535
drop_index = 44826
movies.loc[row_index, 'popularity'] = new_value
movies.drop(labels = drop_index, inplace = True)

# Unión de los dataframes
merged_df = movies.merge(credits, on = 'id', how = 'outer')
merged_df = merged_df.drop(['collection'], axis = 1)

# Completando datos faltantes con TMDB API
merged_df.loc[19721, 'title'] = 'Midnight Man'
merged_df.loc[19721, 'release_date'] = pd.Timestamp('1997-08-20')
merged_df.loc[19721, 'runtime'] = 104.0

merged_df.loc[29481, 'title'] = 'Mardock Scramble: The Third Exhaust'
merged_df.loc[29481, 'release_date'] = pd.Timestamp('2012-09-29')
merged_df.loc[29481, 'runtime'] = 66.0

merged_df.loc[35561, 'title'] = 'Avalanche Sharks'
merged_df.loc[35561, 'release_date'] = pd.Timestamp('2014-01-12')
merged_df.loc[35561, 'runtime'] = 80.0

url_base = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')

for i, row in merged_df.iterrows():
  title = row['title']
  release_date = row['release_date']
  if pd.isna(release_date):
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
          release_date_str = data['release_date']
          if release_date_str:
            release_date = pd.to_datetime(release_date_str)
            merged_df.at[i, 'release_date'] = release_date
            
            
# Reemplazar los valores encontrados respecto al index 711
merged_df.loc[711, 'release_date'] = pd.Timestamp('1995-09-09')
merged_df.loc[711, 'director'] = 'Gaylene Preston'
merged_df.loc[711, 'genres'] = 'Documentary, Romance, War'
# Reemplazar los valores encontrados respecto al index 20292
merged_df.loc[20292, 'release_date'] = pd.Timestamp('1995-01-01')
merged_df.loc[20292, 'director'] = 'Tim Curran'
merged_df.loc[20292, 'runtime'] = 45.0
merged_df.loc[20292, 'genres'] = 'Documentary'
# Reemplazar los valores encontrados respecto al index 20622
merged_df.loc[20622, 'release_date'] = pd.Timestamp('2009-04-10')
merged_df.loc[20622, 'director'] = 'Graham Elwood'
# Reemplazar los valores encontrados respecto al index 21154
merged_df.loc[21154, 'release_date'] = pd.Timestamp('2007-03-20')
merged_df.loc[21154, 'director'] = 'Robert Dixon'
# Reemplazar los valores encontrados respecto al index 27480
merged_df.loc[27480, 'release_date'] = pd.Timestamp('2008-10-12')
merged_df.loc[27480, 'director'] = 'John Paul Davidson'
merged_df.loc[27480, 'genres'] = 'Documentary'
# Reemplazar los valores encontrados respecto al index 32715
merged_df.loc[32715, 'release_date'] = pd.Timestamp('2015-03-15')
merged_df.loc[32715, 'actors'] = 'David Morrison, John W. Boyd, Simon P. Worden'
# Reemplazar los valores encontrados respecto al index 34220
merged_df.loc[34220, 'release_date'] = pd.Timestamp('1977-06-01')
merged_df.loc[34220, 'genres'] = 'Drama, Romance'
merged_df.loc[34220, 'runtime'] = 93.0
# Reemplazar los valores encontrados respecto al index 34415
merged_df.loc[34415, 'release_date'] = pd.Timestamp('2013-07-23')
merged_df.loc[34415, 'genres'] = 'Documentary'
merged_df.loc[34415, 'director'] = 'Ema Ryan Yamazaki'
# Reemplazar los valores encontrados respecto al index 36394
merged_df.loc[36394, 'release_date'] = pd.Timestamp('2014-06-14')
merged_df.loc[36394, 'runtime'] = 9.0
merged_df.loc[36394, 'director'] = 'Thierry Terrasson Jim'
merged_df.loc[36394, 'overview'] = 'The meeting of two worlds opposed to a red light, between a pretty young woman in a car and SDF. A film filled with tenderness, with beautiful images on a topic of precariousness. It causes you to turn round in an idyllic set on the sidewalk as curious pedestrian or as a stowaway in the cabin of the conductor.'
merged_df.loc[36394, 'genres'] = 'Short, Comedy, Romance'
# Reemplazar los valores encontrados respecto al index 37187
merged_df.loc[37187, 'release_date'] = pd.Timestamp('2001-12-06')
merged_df.loc[37187, 'director'] = 'Frank van den Engel'
merged_df.loc[37187, 'runtime'] = 82.0
merged_df.loc[37187, 'genres'] = 'Documentary'
# Reemplazar los valores encontrados respecto al index 38302
merged_df.loc[38302, 'release_date'] = pd.Timestamp('2002-06-20')
merged_df.loc[38302, 'director'] = 'Kôichi Mashimo, Masayuki Yoshihara'
merged_df.loc[38302, 'genres'] = 'Animation, Drama, Mystery, Science Fiction'
# Reemplazar los valores encontrados respecto al index 39576
merged_df.loc[39576, 'release_date'] = pd.Timestamp('2013-03-02')
merged_df.loc[39576, 'genres'] = 'Documentary'
# Reemplazar los valores encontrados respecto al index 41039
merged_df.loc[41039, 'release_date'] = pd.Timestamp('2000-01-01')
merged_df.loc[41039, 'runtime'] = 70.0
merged_df.loc[41039, 'director'] = 'Scott Zakarin'
merged_df.loc[41039, 'genres'] = 'Comedy, Family, Fantasy'
merged_df.loc[41039, 'production_companies'] = 'Walt Disney Productions'
# Reemplazar los valores encontrados respecto al index 42538
merged_df.loc[42538, 'release_date'] = pd.Timestamp('2012-09-18')
merged_df.loc[42538, 'genres'] = 'Family'
# Reemplazar los valores encontrados respecto al index 42543
merged_df.loc[42543, 'title'] = 'When the Day Had No Name'
merged_df.loc[42543, 'release_date'] = pd.Timestamp('2017-02-11')
merged_df.loc[42543, 'runtime'] = 93.0
merged_df.loc[42543, 'genres'] = 'Drama'
merged_df.loc[42543, 'director'] = 'Teona Strugar Mitevska'
merged_df.loc[42543, 'overview'] = 'Day before Easter 2012, perfectly lined up bodies of four teenagers, each with a bullet hole in their head, were found near a lake just outside Skopje, Macedonian capital. They just went fishing. The nation was shocked. The rumours run wild. Ethnic tensions were boiling. The police investigation, officially named "Monsters", pointed to Islamists terrorists. Two years later, court jailed four persons for murder and terrorism. The alleged perpetrators deny the act. This film is fiction about what could have happened that day, those hours before the tragedy stroke. Through the film we live the last day in the life of six youngsters. It is a reconstruction of Macedonian grim reality, not of the actual events. It is a film about a country where life can cease suddenly without a cause, as it is lived.'
# Reemplazar los valores encontrados respecto al index 42911
merged_df.loc[42911, 'release_date'] = pd.Timestamp('1978-10-27')
merged_df.loc[42911, 'director'] = 'Stein Roger Bull'
merged_df.loc[42911, 'genres'] = 'Horror, Mystery, Science Fiction, Thriller'
merged_df.loc[42911, 'runtime'] = 110.0
# Reemplazar los valores encontrados respecto al index 43932
merged_df.loc[43932, 'release_date'] = pd.Timestamp('2013-05-30')
merged_df.loc[43932, 'director'] = 'Jordan Stone'
merged_df.loc[43932, 'genres'] = 'Documentary, Biography'
# Reemplazar los valores encontrados respecto al index 44068
merged_df.loc[44068, 'title'] = 'Igra na vybyvanie'
merged_df.loc[44068, 'release_date'] = pd.Timestamp('2005-12-08')
merged_df.loc[44068, 'director'] = 'Vadim Shmelev'
merged_df.loc[44068, 'genres'] = 'Thriller'
# Reemplazar los valores encontrados respecto al index 44768
merged_df.loc[44768, 'release_date'] = pd.Timestamp('2004-07-01')
merged_df.loc[44768, 'director'] = 'David Firth'
# Reemplazar los valores encontrados respecto al index 45038
merged_df.loc[45038, 'release_date'] = pd.Timestamp('2017-05-11')
merged_df.loc[45038, 'director'] = 'Josias Teófilo'
merged_df.loc[45038, 'genres'] = 'Documentary'
merged_df.loc[45038, 'runtime'] = 81.0

merged_df = merged_df.dropna(subset = ['release_date'])
# Limpiar los valores faltantes de la columna 'overview'
merged_df['overview'] = merged_df['overview'].apply(lambda x: str(x).strip())
merged_df['overview'] = merged_df['overview'].apply(lambda x: re.sub(r'[^\w\s]','',x))
merged_df['overview'] = merged_df['overview'].apply(lambda x: x.lower())

# Reemplazar los valores faltantes con 'No overview found' o NaN
merged_df['overview'] = merged_df['overview'].apply(lambda x: 'no overview found' if x in ['nan', 'no overview', 'no overview found', 'no movie overview available', None] else x)
merged_df['overview'] = merged_df['overview'].apply(lambda x: np.nan if x == '' else x)


for i, row in merged_df.iterrows():
  title = row['title']
  genres = row['genres']
  if pd.isna(genres):
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
          genres = [genre['name'] for genre in data['genres']]
          merged_df.at[i, 'genres'] = ', '.join(genres[:3])
          
merged_df['genres'] = merged_df['genres'].replace('', np.nan)
merged_df['genres'] = merged_df['genres'].apply(ut.strip_genres)
duplicates = merged_df['genres'].apply(ut.has_duplicates)
merged_df['genres'] = merged_df['genres'].apply(ut.lower_case_genres)
mask = (merged_df['runtime'].isnull()) | (merged_df['runtime'] == 0)
merged_df.loc[mask, 'runtime'] = merged_df.loc[mask, 'title'].apply(lambda title: ut.get_runtime(title, api_key, url_base))