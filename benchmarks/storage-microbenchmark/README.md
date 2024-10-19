
This benchmark was executed on the AWS `c3.xlarge` VM instance, with AWS S3 and DynamoDB. For Redis, we deployed
Redis 7.4 container on the `c3.xlarge` container.

## Preparation

Create S3 bucket, and a DynamoDB table with serverless provisioning.

Create Lambda function, set memory, and add permision to access DynamoDB and S3.
Install `pip install boto3 py-redis`, pack together with the code, and upload to Lambda.
Lambda function should run Python 3.10, have 2 GB of memory, and the handler is `benchmark.lambda_handler`.

## Redis

* On the VM hosting Redis (c4x.l), install Docker and allow inbound traffic on port 6379.
* Run `docker run --name redis -v $PWD/data:/data -p 6379:6379  -d redis:7.4 redis-server --requirepass <pass>`
* Update `config.json` with IP address and the password.

## Execution

```
python benchmarker.py config.json redis
python benchmarker.py config.json s3
python benchmarker.py config.json dynamodb
```

### S3

* Change the bucket name in `benchmark.json`.
* Execute `python `

## Our config

* Region: `us-east-1`
* Redis: `c3.xlarge` 
* Python: 3.10
* boto3: `1.35`
* Redis: `5.1.1`

