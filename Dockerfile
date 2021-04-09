FROM python:3.9-slim
LABEL name="cfunkhouser/octodns-sync-action"
LABEL maintainer="Christian Funkhouser <christian@funkhouse.rs>"

COPY . /src

RUN python -m pip install --upgrade pip \
    && python -m pip install /src/.

ENTRYPOINT [ "python", "-m", "octosync", "--octodns_config_file" ]
