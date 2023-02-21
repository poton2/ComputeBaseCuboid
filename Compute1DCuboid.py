import argparse
import datetime
import numpy as np
import pandas as pd
import os
import glob


def generate1DCuboid(twoD_cuboid_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    USER_CUBOID = os.path.join(output_directory, 'user')
    YEAR_CUBOID = os.path.join(output_directory, 'year')
    MOVIE_CUBOID = os.path.join(output_directory, 'movie')
    if not os.path.exists(USER_CUBOID):
        os.makedirs(USER_CUBOID)
    if not os.path.exists(YEAR_CUBOID):
        os.makedirs(YEAR_CUBOID)
    if not os.path.exists(MOVIE_CUBOID):
        os.makedirs(MOVIE_CUBOID)

    for dirpath, dirnames, filenames in os.walk(twoD_cuboid_directory):
        ## user
        if os.path.basename(dirpath) == 'user_movie':
            dfs = []
            for file_path in glob.glob(os.path.join(dirpath, '*.txt')):
                data = pd.read_csv(file_path, sep='\t')
                dfs.append(data)

            df = pd.concat(dfs, ignore_index=True)
            user_cuboid = df.groupby(['user_id'])['avg_rating'].agg(['mean']).reset_index()
            user_cuboid['total_count'] = df.groupby('user_id')['count'].sum().values
            user_cuboid.rename(columns={'mean': 'avg_rating'}, inplace=True)
            user_cuboid_parts = np.array_split(user_cuboid, 10)

            for i, part in enumerate(user_cuboid_parts):
                output_file = os.path.join(USER_CUBOID, f"{i + 1}.txt")
                part.to_csv(output_file, sep='\t', index=False)
        ## year/movie
        if os.path.basename(dirpath) == 'movie_year':
            dfs = []
            for file_path in glob.glob(os.path.join(dirpath, '*.txt')):
                data = pd.read_csv(file_path, sep='\t')
                dfs.append(data)

            df = pd.concat(dfs, ignore_index=True)
            year_cuboid = df.groupby(['year'])['avg_rating'].agg(['mean']).reset_index()
            year_cuboid['total_count'] = df.groupby('year')['count'].sum().values
            year_cuboid.rename(columns={'mean': 'avg_rating'}, inplace=True)

            output_file = os.path.join(YEAR_CUBOID, f"{1}.txt")
            year_cuboid.to_csv(output_file, sep='\t', index=False)

            movie_cuboid = df.groupby(['movie_id'])['avg_rating'].agg(['mean']).reset_index()
            movie_cuboid['total_count'] = df.groupby('movie_id')['count'].sum().values
            movie_cuboid.rename(columns={'mean': 'avg_rating'}, inplace=True)
            movie_cuboid_parts = np.array_split(movie_cuboid, 10)

            for i, part in enumerate(movie_cuboid_parts):
                output_file = os.path.join(MOVIE_CUBOID, f"{i + 1}.txt")
                part.to_csv(output_file, sep='\t', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file directory')
    parser.add_argument('-o', '--output', required=True, help='Output directory path')
    args = parser.parse_args()
    generate1DCuboid(args.input, args.output)
