FROM python:3.9-slim
ARG image_version
LABEL name="cfunkhouser/octodns-sync-action"
LABEL version="${image_version}"
LABEL maintainer="Christian Funkhouser <christian@funkhouse.rs>"

COPY . /src

RUN python -m pip install --upgrade pip \
    && python -m pip install /src/.

ENTRYPOINT [ "python", "-m", "octosync", "--config_file" ]
