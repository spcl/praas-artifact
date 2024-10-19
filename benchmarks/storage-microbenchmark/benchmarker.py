import boto3
import json
import csv
import sys

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def invoke_lambda(lambda_client, function_name, payload):
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.loads(response['Payload'].read())

def run_benchmark(config, experiment, lambda_client):
    results = []
    for size in config['data_sizes']:

        payload = {
            'experiment': experiment,
            'size': size,
            'iterations': config['iterations'],
            's3_bucket': config['s3_bucket'],
            'dynamodb_table': config['dynamodb_table'],
            'redis': config['redis']
        }
        response = invoke_lambda(lambda_client, config['lambda_function_name'], payload)
        if response['statusCode'] == 200:
            data = json.loads(response['body'])
            for time, s in zip(data['times'], data['sizes']):
                results.append({
                    'experiment': experiment,
                    'size': size,
                    'time_us': time,
                    'output_size': s
                })
        else:
            print(f"Error in Lambda execution: {response['body']}")

    return results

def save_results(results, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['experiment', 'size', 'time_us', 'output_size'])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client_script.py <config_file> <experiment>")
        sys.exit(1)

    config_file = sys.argv[1]
    experiment = sys.argv[2]
    config = load_config(config_file)

    lambda_client = boto3.client('lambda')
    results = run_benchmark(config, experiment, lambda_client)
    save_results(results, f"{experiment}_benchmark_results.csv")
    print("Benchmark complete. Results saved to benchmark_results.csv")

