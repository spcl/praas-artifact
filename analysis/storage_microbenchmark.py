import pandas as pd
import os

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    df['size_kb'] = df['size'] / 1024
    df['time_us'] = df['time_us'] / 1000.0
    return df

dfs = []
for mode in ['redis', 's3', 'dynamodb']:

    path = os.path.join(os.path.pardir, 'data', 'storage_microbenchmark', f'{mode}_benchmark_results.csv')
    dfs.append(load_and_process_data(path))

df = pd.concat(dfs)

print('Mean')
print(df.groupby(['experiment', 'size'])['time_us'].mean())

print('Median')
print(df.groupby(['experiment', 'size'])['time_us'].median())

print('Stdev')
print(df.groupby(['experiment', 'size'])['time_us'].std())
