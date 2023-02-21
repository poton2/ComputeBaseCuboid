import argparse
import argparse
import numpy as np
import pandas as pd
import os


def computeApex(oneD_cuboid_directory):
    for dirpath, dirnames, filenames in os.walk(os.path.join(oneD_cuboid_directory, 'year')):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            df = pd.read_csv(fullpath, sep='\t')
            print('Total count:', df['total_count'].sum())

            # print total average
            print('Total average:', df['avg_rating'].mean())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file directory')
    args = parser.parse_args()
    computeApex(args.input)
