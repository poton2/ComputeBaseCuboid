import argparse
import datetime
import numpy as np
import pandas as pd
import os


def generate_base_cuboid(input_directory, output_directory):
    path = input_directory + "/ratings.txt"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    df = pd.read_csv(path, engine='python', sep='::', names=['user_id', 'movie_id', 'rating', 'year'])
    df['year'] = df['year'].apply(datetime.datetime.utcfromtimestamp)
    df['year'] = df['year'].dt.year
    base_cuboid = df.groupby(['user_id', 'movie_id', 'year']).agg({'rating': ['mean', 'count']})
    base_cuboid.columns = ['avg_rating', 'num_ratings']

    print(base_cuboid)

    users = base_cuboid.index.get_level_values('user_id').unique().sort_values()
    movies = base_cuboid.index.get_level_values('movie_id').unique().sort_values()
    years = base_cuboid.index.get_level_values('year').unique().sort_values()

    user_partitions = np.array_split(users, 5)
    movies_partitions = np.array_split(movies, 5)
    years_partitions = np.array_split(years, 4)

    chunk_id = 1
    for i, year_chunk in enumerate(years_partitions):
        for j, movie_chunk in enumerate(movies_partitions):
            for k, user_chunk in enumerate(user_partitions):
                # Select only the rows that belong to this chunk
                chunk_df = base_cuboid.loc[(user_chunk, movie_chunk, year_chunk), :]

                # Write the chunk to a file
                chunk_filename = f"{chunk_id}.csv"
                chunk_path = os.path.join(output_directory, chunk_filename)
                chunk_df.to_csv(chunk_path)

                chunk_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory path')
    args = parser.parse_args()
    generate_base_cuboid(args.input, args.output)
