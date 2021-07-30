ARG BASE_IMAGE
FROM ${BASE_IMAGE}
WORKDIR /app
COPY . ./
RUN chmod +x ./setup.sh
RUN ./setup.sh
RUN chmod +x ./run.sh
CMD tail -f /dev/null
