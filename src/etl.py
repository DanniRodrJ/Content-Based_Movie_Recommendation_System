import os
import ast
import re
import numpy as np
import pandas as pd
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data(data_dir: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load CSV files into DataFrames."""
    logger.info("Loading data files...")
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    credits_path = os.path.join(data_dir, 'credits.csv')
    movies_path = os.path.join(data_dir, 'movies_dataset.csv')
    
    credits_df = pd.read_csv(credits_path)
    movies_df = pd.read_csv(movies_path, low_memory=False)
    
    logger.info(f"Loaded {len(credits_df)} credits records and {len(movies_df)} movies records")
    return credits_df, movies_df


def extract_director(crew_data: Any) -> Optional[str]:
    """Extract director name from crew data."""
    if not isinstance(crew_data, list) or len(crew_data) == 0:
        return None
    
    directors = [member['name'] for member in crew_data if member.get('job') == 'Director']
    return ', '.join(directors) if directors else None


def extract_actors(cast_data: Any) -> Optional[str]:
    """Extract actor names from cast data."""
    if not isinstance(cast_data, list) or len(cast_data) == 0:
        return None
    
    actors = [member['name'] for member in cast_data if member.get('name')]
    return ', '.join(actors) if actors else None


def parse_json_column(value: Any) -> Any:
    """Parse stringified JSON/list values to Python objects."""
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return None
    return None


def extract_collection_name(data: Any) -> Optional[str]:
    """Extract collection name from belongs_to_collection dict."""
    if isinstance(data, dict) and 'name' in data:
        return data['name']
    return None


def extract_genres(data: Any) -> Optional[str]:
    """Extract genre names from genres list."""
    if isinstance(data, list) and len(data) > 0:
        genres = [item.get('name', '') for item in data if item.get('name')]
        return ', '.join(genres) if genres else None
    return None


def extract_production_companies(data: Any) -> Optional[str]:
    """Extract production company names."""
    if isinstance(data, list) and len(data) > 0:
        companies = [item.get('name', '') for item in data if item.get('name')]
        return ', '.join(companies) if companies else None
    return None


def extract_production_countries(data: Any) -> Optional[str]:
    """Extract production country names."""
    if isinstance(data, list) and len(data) > 0:
        countries = [item.get('name', '') for item in data if item.get('name')]
        return ', '.join(countries) if countries else None
    return None


def extract_spoken_languages(data: Any) -> Optional[str]:
    """Extract spoken language names."""
    if isinstance(data, list) and len(data) > 0:
        languages = [item.get('name', '') for item in data if item.get('name')]
        return ', '.join(languages) if languages else None
    return None


def process_credits(credits_df: pd.DataFrame) -> pd.DataFrame:
    """Process credits DataFrame - extract directors and actors."""
    logger.info("Processing credits data...")
    
    credits_copy = credits_df.copy()
    
    credits_copy['cast'] = credits_copy['cast'].apply(parse_json_column)
    credits_copy['crew'] = credits_copy['crew'].apply(parse_json_column)
    
    credits_copy['director'] = credits_copy['crew'].apply(extract_director)
    credits_copy['actors'] = credits_copy['cast'].apply(extract_actors)
    
    credits_clean = credits_copy[['id', 'director', 'actors']].copy()
    
    credits_clean = credits_clean.drop_duplicates(subset='id', keep='first')
    
    logger.info(f"Processed {len(credits_clean)} unique credits records")
    return credits_clean


def process_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
    """Process movies DataFrame - clean and extract nested data."""
    logger.info("Processing movies data...")
    
    movies_copy = movies_df.copy()
    
    columns_to_drop = ['adult', 'imdb_id', 'homepage', 'original_title', 'poster_path', 'video']
    movies_copy = movies_copy.drop(columns=[c for c in columns_to_drop if c in movies_copy.columns], errors='ignore')
    
    movies_copy['original_language'] = movies_copy['original_language'].astype(str)
    movies_copy.loc[movies_copy['original_language'].apply(lambda x: bool(re.search(r'\d', x))), 'original_language'] = np.nan
    
    movies_copy.loc[movies_copy['overview'].str.strip() == '', 'overview'] = np.nan
    movies_copy['tagline'] = movies_copy['tagline'].replace('-', np.nan)
    
    json_columns = ['belongs_to_collection', 'genres', 'production_companies', 'production_countries', 'spoken_languages']
    for col in json_columns:
        if col in movies_copy.columns:
            movies_copy[col] = movies_copy[col].apply(parse_json_column)
    
    movies_copy['collection'] = movies_copy['belongs_to_collection'].apply(extract_collection_name)
    movies_copy['genres'] = movies_copy['genres'].apply(extract_genres)
    movies_copy['production_companies'] = movies_copy['production_companies'].apply(extract_production_companies)
    movies_copy['production_countries'] = movies_copy['production_countries'].apply(extract_production_countries)
    movies_copy['spoken_languages'] = movies_copy['spoken_languages'].apply(extract_spoken_languages)
    
    movies_copy = movies_copy.drop(columns=['belongs_to_collection'], errors='ignore')
    
    logger.info(f"Processed {len(movies_copy)} movies records")
    return movies_copy


def merge_data(movies_df: pd.DataFrame, credits_df: pd.DataFrame) -> pd.DataFrame:
    """Merge movies and credits DataFrames on 'id' column."""
    logger.info("Merging movies and credits data...")
    
    merged_df = movies_df.merge(credits_df, on='id', how='left')
    
    logger.info(f"Merged dataset contains {len(merged_df)} records")
    return merged_df


def run_etl(data_dir: str, output_path: str) -> pd.DataFrame:
    """
    Main ETL pipeline execution.
    
    Args:
        data_dir: Directory containing input CSV files
        output_path: Path to save the final merged dataset
    
    Returns:
        Merged DataFrame
    """
    logger.info("Starting ETL pipeline...")
    
    credits_df, movies_df = load_data(data_dir)
    
    credits_processed = process_credits(credits_df)
    movies_processed = process_movies(movies_df)
    
    final_df = merge_data(movies_processed, credits_processed)
    
    if output_path:
        final_df.to_csv(output_path, index=False)
        logger.info(f"Saved final dataset to {output_path}")
    
    logger.info("ETL pipeline completed successfully!")
    return final_df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ETL Pipeline for Movie Data')
    parser.add_argument('--data_dir', type=str, default='./Dataset', help='Input data directory')
    parser.add_argument('--output', type=str, default='./movies_merged.csv', help='Output file path')
    
    args = parser.parse_args()
    
    result_df = run_etl(args.data_dir, args.output)
    print(f"\nFinal dataset shape: {result_df.shape}")
    print(f"\nColumns: {result_df.columns.tolist()}")