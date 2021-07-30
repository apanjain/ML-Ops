# Model Train Bot

## Dedicated container to serve a model train request

### Description

- This container is spun up through the kube-deployer application (aka autosacler bot) to process a sigle user's reuqest.
- It contains a shell script which takes in arguments three parameters `train_file_location`, `train_file_name` and `ml_user` as environment variables.
- The scripts goes to the `user/uploads` directory and creates & activates a virtual environment.
- Then it installs all the dependencies mentioned in the `requirements.txt` file (persisted to make future trainings faster).
- After this it goes to the subdirectory where the training code exists (`train.py`) and executes that file.
- The logs generated from all these operations and the print statements inside the training code are redirected to a `training.log` file in the same subdirectory, (the same is displayed on the frontend).

### Setup

- No additional setup, just build and push the image to GCR.

```bash
cd model-trainer
```

```bash
gcloud builds submit --tag $ML_TRAIN_IMAGE .
```

### Usage

- Usage is taken care of by the kube-deployer ;)

### Furthur work

- This image is python specific but a similar implementaion can be done for other languages as well.
- The `image-build` folder contains instructions and code for dynamically creating images.
