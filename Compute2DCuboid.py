import argparse
import numpy as np
import pandas as pd
import os


def generate_2d_cuboids(base_cuboid_directory, output_directory):
    # create output directories if they don't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    user_movie_dir = os.path.join(output_directory, 'user_movie')
    user_year_dir = os.path.join(output_directory, 'user_year')
    movie_year_dir = os.path.join(output_directory, 'movie_year')
    if not os.path.exists(user_movie_dir):
        os.makedirs(user_movie_dir)
    if not os.path.exists(user_year_dir):
        os.makedirs(user_year_dir)
    if not os.path.exists(movie_year_dir):
        os.makedirs(movie_year_dir)

        # read base cuboid chunk by chunk
    for filename in os.listdir(base_cuboid_directory):
        base_cuboid_chunk = pd.read_csv(os.path.join(base_cuboid_directory, filename))

        # generate user-movie cuboid
        user_movie_cuboid_chunk = base_cuboid_chunk.groupby(['user_id', 'movie_id']).agg(
            {'avg_rating': ['mean', 'count']}).reset_index()
        user_movie_cuboid_chunk.columns = ['user_id', 'movie_id', 'avg_rating', 'count']
        user_movie_cuboid_chunk.to_csv(os.path.join(user_movie_dir, filename[:-4] + '.txt'), header=True,
                                       index=False, sep='\t')
        print(f'User-Movie Cuboid - {filename[:-4]}: {len(user_movie_cuboid_chunk)} records')

        # generate user-year cuboid
        user_year_cuboid_chunk = base_cuboid_chunk.groupby(['user_id', 'year']).agg(
            {'avg_rating': ['mean', 'count']}).reset_index()
        user_year_cuboid_chunk.columns = ['user_id', 'year', 'avg_rating', 'count']
        user_year_cuboid_chunk.to_csv(os.path.join(user_year_dir, filename[:-4] + '.txt'), header=True,
                                      index=False, sep='\t')
        print(f'User-Year Cuboid - {filename[:-4]}: {len(user_year_cuboid_chunk)} records')

        # generate movie-year cuboid
        movie_year_cuboid_chunk = base_cuboid_chunk.groupby(['movie_id', 'year']).agg(
            {'avg_rating': ['mean', 'count']}).reset_index()
        movie_year_cuboid_chunk.columns = ['movie_id', 'year', 'avg_rating', 'count']
        movie_year_cuboid_chunk.to_csv(os.path.join(movie_year_dir, filename[:-4] + '.txt'), header=True,
                                       index=False, sep='\t')
        print(f'Movie-Year Cuboid - {filename[:-4]}: {len(movie_year_cuboid_chunk)} records')

        # discard base cuboid chunk
        del base_cuboid_chunk


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory path')
    args = parser.parse_args()
    generate_2d_cuboids(args.input, args.output)
