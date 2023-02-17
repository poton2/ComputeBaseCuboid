import argparse

import numpy as np
import pandas as pd
import csv
import datetime
import os
from collections import defaultdict


def generate_base_cuboid(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            ratings = pd.read_csv(file_path, sep='::', engine='python', header=None,
                                  names=['user_id', 'movie_id', 'rating', 'timestamp'])
            ratings['year'] = pd.to_datetime(ratings['timestamp'], unit='s').dt.year

            base_cuboid = ratings.groupby(['user_id', 'movie_id', 'year']).agg({'rating': ['mean', 'count']})
            base_cuboid.columns = ['avg_rating', 'num_ratings']

            # Partition on sorted array of unique values in each dimension
            users = base_cuboid.index.get_level_values('user_id').unique().sort_values()
            movies = base_cuboid.index.get_level_values('movie_id').unique().sort_values()
            years = base_cuboid.index.get_level_values('year').unique().sort_values()

            user_partitions = np.array_split(users, 5)
            movies_partitions = np.array_split(movies, 5)
            years_partition = np.array_split(years, 4)

            chunk_id = 1
            for i, user_chunk in enumerate(user_partitions):
                for j, movie_chunk in enumerate(movies_partitions):
                    for k, year_chunk in enumerate(years_partition):
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

