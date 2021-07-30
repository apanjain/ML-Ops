# Training & Prediction API

## Flask API service to send training message and make predictions

### Description

- Just like the training bot, this application also has access to the shared storage where the user puts his training and prediciton files.
- It is mainly divided into two segments, training and predicition APIs, that are hosted from the same flask app, along with their respective frontend interfaces.

### Frontend

- Frontend is basically a combination of two forms which can be accessed on `/training` and `/prediction` url.
- The training form takes three input parameters
  from the user, the `username`, the `training file name` (usually 'train.py') and the `training file location `(usually '.') {relative to the uploads folder in the sftp server for the corresponding user}
- Once the user hits Train button, they can see the logs generated while training the model on the same page itself.
- The prediction form take in input three similar parameters as training form, the `username`, the `prediction file name` {without .py extension} (usually 'prediciton') and the `prediction file location`
- Additionaly user can add key/value pairs using the `Add +` button, which can be used by the prediction file in the shared storage as a python dictionary.

### Backend

- The backend handles the training request recieved from the training form and sends a message to the kafka broker for the same.
- This is served by the `/train/<user>` url. This method uses the `secure_producer` file to send the message.
- The training logs are fetched using `/logs/<user>` url, by making regular requests until it receives a stop signal.
- The backend also handles prediction request received from the prediction from on `/predict/<user>` url.
- This method leverages the virtual environment created during the training by adding the path for those site-packages in `sys.path` variable.
- The `predict` function in the prediction file (details about creating such file are mentioned in the test-user section) is then called with the key/value pairs from the request as arguments and the response is then forwarded to the user in the plain text format.

### Setup & Usage

- First create an image from this folder and push it to GCR by executing the following commands

```bash
cd prediction
```

```bash
gcloud builds submit --tag gcr.io/$GCLOUD_PROJECT_ID/$ML_PREDICTION_IMAGE
```

- Here the `ML_PREDICTION_IMAGE` is the image name.
- Access the shared storage (persistent disk) of the ftp server, (not by sftp login) and place the `ca-cert` file of the kafka broker somewhere in that storage, this will be used by our `secure_producer`.
  - One way can be
  ```bash
    kubectl cp <path_to_ca-cert_on_local_machine> <ftp_pod_id>:/mnt/c/<path_to_paste_the_file>
  ```
- Next, update the `ml-pred-depl.yaml` file by replacing the name of the $ML_PREDICTION_IMAGE with the actual name.
- Also add Kafka connection parameters, to access the brokers.
- Here `KAFKA_BOOTSTRAP_SERVERS` is the string of space separated IP addresses on which the kafka brokers are listening.
- Now since we are mounting the shared storage on the path `/mnt/c`, the value of `CA_CERT_LOCATION` will be something like `/mnt/c/<path to ca-cert inside shared storage>`.
- Rest of the other parameters are what you can get while setting up the KAFKA cluster (refer to the kafka-setup folder).
- Lastly, replace the `FTP_SERVER_CLAIM_NAME` by the claim generated for the FTP storage.
- Then run the following command to start the container.

```bash
kubectl apply -f ./ml-pred-depl.yaml
```

- Then run the following command to get the external ip of your ml-pred pod (can take upto 1 minute).

```bash
kubectl get services
```

- Visit this external IP to consume the services on the exposed URLs.
