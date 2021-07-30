# ML Framework Solution

## Production level solution for automating training of already developed models

## Architecture Diagram

![alt text](https://github.com/apanjain/ML-Ops/blob/master/architecture-diagram.png?raw=true)

### Description

- Easy to setup Kubernetes solution which provides a ready to use environment for training complex ML algorithms.
- High Availiblity API service for fast training and prediction of ML models.
- Resource consumption is optimized by on demand resource allocation.
- Can be easily integrated to pre-existing automation solutions.
- Customized kafka cluster with secure communication protocols.
- Highly scalable and language agnostic.

### Setup Instructions

- Each component of this solution has it's own README file containing the description, setup, and usage.
- Follow the Readme files and setup these components in the following order.
  - [`kafka-setup`](https://github.com/apanjain/ML-Ops/tree/master/kafka-setup#readme) (KAFKA CLUSTER)
  - [`ftp-server`](https://github.com/apanjain/ML-Ops/tree/master/ftp-server#readme)
  - [`model-trainer`](https://github.com/apanjain/ML-Ops/tree/master/model-trainer#readme)
  - [`kube-deployer`](https://github.com/apanjain/ML-Ops/tree/master/kube-deployer#readme)
  - [`prediction`](https://github.com/apanjain/ML-Ops/tree/master/prediction)

### Usage

- Then take the [`test-user`](https://github.com/apanjain/ML-Ops/tree/master/test-user) files and upload it to the SFTP folder of one of the user.
- Execute the training and prediction through the frontend application or the API service provided.
