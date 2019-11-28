ARG BASE_IMAGE=circleci/python:3.7

FROM ${BASE_IMAGE}
FROM circleci/python:3.7
MAINTAINER rumble.travel <juan@rumble.travel>
# Version 1.0

ARG GDAL_VERSION=2.3.3

# Fetch & install dependencies
RUN sudo apt-get update
RUN sudo apt-get install -y --no-install-recommends apt-utils
RUN sudo apt-get install -y --no-install-recommends \
        gdal-bin binutils libproj-dev libgdal-dev libgeos-dev

# Install latest Numpy
RUN pip install --user numpy

# Install Python GDAL
RUN pip install --user GDAL==${GDAL_VERSION}

# Clean up
RUN sudo apt-get autoremove -y
RUN sudo rm -rf /var/apt/lists/*
RUN sudo rm -rf /var/cache/apt/*

CMD python3 -V && pip -V && gdalinfo --version
