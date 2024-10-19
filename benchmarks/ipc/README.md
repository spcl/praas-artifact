

* PraaS repository: `benchmarks` branch.
* Functions source code: `benchmarks/ipc/functions`
* Benchmarks source code:  `benchmarks/ipc/`
* Container build?: `benchmarks` branch, `process/docker/Dockerfile.process-ipc`. First might be needed to build the images with cpp builder and dependencies.
  ```
  docker build -f process/docker/Dockerfile.process-ipc -t spcleth/praas-examples:process-ipc.
  ```
* Original image: `spcleth/praas-examples:process-ipc`
