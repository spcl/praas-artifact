

* PraaS repository: `benchmarks` branch.
* Functions source code: `benchmarks/functions`
* Benchmarks source code:  `benchmarks/`. `benchmarks/invocations_benchmarker.cpp` for remote invocations, and `benchmarks/local_invocations_benchmarker.cpp` for local invocations.
* Container build?: `benchmarks` branch, `process/docker/Dockerfile.process`. First might be needed to build the images with cpp builder and dependencies.
  ```
  docker build -f process/docker/Dockerfile.process-ipc -t spcleth/praas-examples:process.
  ```
* Original image: `spcleth/praas-examples:process`

## Ethernet

Inside the Fargate container, run `netserver`. Then, from the source machine run `ethernet.sh <size>`

Make sure the container's security group can accept inbound conenctions at netperf's port.

## Lambda

Run the scripts in this order:
* Build SDK.
* Build functions.
* Create function (uncomment the options to create role and Lambda functions, changing the `<user-id>`.
* Build the tester.
* Replace Lambda URL in the `tester.sh` and run it.
