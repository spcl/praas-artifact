import boto3
import redis
import json
from datetime import datetime, timedelta

def generate_data(size):
    return 'x' * size

def benchmark_s3(bucket_name, data, n):
    s3 = boto3.client('s3')
    key = f"benchmark_data_{len(data)}"

    s3.put_object(Bucket=bucket_name, Key=key, Body=data)

    sizes = []
    times = []
    for i in range(n + 1):
        begin = datetime.now()
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = response['Body'].read()
        end = datetime.now()
        if i > 0:
            times.append((end - begin) / timedelta(microseconds=1))
            sizes.append(len(data))

    #s3.delete_object(Bucket=bucket_name, Key=key)

    return times, sizes

def benchmark_dynamodb(table_name, data, n):

    if len(data) > 200 * 1024:
        return [], []

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    key = f"benchmark_data_{len(data)}"
    item = {
        'id': key,
        'data': data
    }
    table.put_item(Item=item)

    sizes = []
    times = []
    for i in range(n + 1):

        begin = datetime.now()
        ret = table.get_item(Key={'id': key})
        end = datetime.now()
        if i > 0:
            times.append((end - begin) / timedelta(microseconds=1))
            sizes.append(len(json.dumps(ret)))

    #table.delete_item(Key={'id': 'benchmark_data'})

    return times, sizes

def benchmark_redis(redis_config, data, n):
    r = redis.Redis(host=redis_config['host'], port=redis_config['port'], password=redis_config['password'])

    key = f"benchmark_data_{len(data)}"
    r.set(key, data)

    sizes = []
    times = []
    for i in range(n + 1):
        begin = datetime.now()
        d = r.get(key)
        end = datetime.now()
        if i > 0:
            times.append((end - begin) / timedelta(microseconds=1))
            sizes.append(len(d))

    #r.delete('benchmark_data')

    return times, sizes


def lambda_handler(event, context):

    experiment = event['experiment']
    size = event['size']

    data = generate_data(size)

    if experiment == 's3':
        times, sizes = benchmark_s3(event['s3_bucket'], data, event['iterations'])
    elif experiment == 'dynamodb':
        times, sizes = benchmark_dynamodb(event['dynamodb_table'], data, event['iterations'])
    elif experiment == 'redis':
        times, sizes = benchmark_redis(event['redis'], data, event['iterations'])
    else:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Unknown experiment type: {experiment}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'experiment': experiment,
            'size': size,
            'times': times,
            'sizes': sizes
        })
    }

