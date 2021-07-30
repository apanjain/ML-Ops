# Setting up the KAFKA CLUSTER
For detail on setting up kafka cluster, you can visit this [github repo](https://github.com/mukesh2966/Kafka-MQ).

Once gone through the details in [kube-demo/setup folder](https://github.com/mukesh2966/Kafka-MQ/tree/main/kube-demo/setup) in the above repo, we can move to utilize the files present in this repo. 

## ENV Varaibles Setup

- Setup these `ENV variables` inside the `zooD0-storage.yaml` file

  - `ZOO_TLS_CLIENT_KEYSTORE_PASSWORD`
  - `ZOO_TLS_CLIENT_TRUSTSTORE_PASSWORD`
  - `PV_CLAIM_NAME_ZOO`


Env variables in each of the kafkaD files are in the same format. So, mentioning the list of env. variables for one of them.

- Setup these `ENV variables` inside the `kafkaD0-storage.yaml` file

  - `KAFKA_CFG_LISTENERS`
  - `KAFKA_CFG_ADVERTISED_LISTENERS`
  - `PV_CLAIM_NAME`

- Setup all the below mentioned fields inside the `per-storage-all.yaml` file

  - `Persistant disk name for each component`
  - `Persistant claim name for each component`
  - `Persistant disk size of each component`
