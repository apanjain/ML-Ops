# Docker Image Build

## Shell script to build a docker image dynamically

### Description

- A dynamic way to create images with any base image and any setup configuration using shell script.
- Uses a template Dockerfile to build an image.

### Setup

- `Docker CLI` should be pre-installed on the machine.
- A directory containing two shell scripts, `run.sh` and `setup.sh`.
- `setup.sh` will contain all the build-side instructions while creating the image, which will replace the `RUN` commands in the `Dockerfile`. It'll setup the environment which can be directly used by the containers.

- `run.sh` will contain all the commands that will be executed after the container is spun up.

### Usage

- After creating both the files mentioned above in a directory, run the below command

```bash
cd image-build
```

```bash
chmod +x ./build.sh
```

```bash
./build.sh <BASE_IMAGE_NAME> <LOCATION_TO_THE_ABOVE_DIRECTOR> <IMAGE_TAG>
```
