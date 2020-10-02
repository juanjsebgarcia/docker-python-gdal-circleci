ARG BASE_IMAGE

FROM ${BASE_IMAGE} as builder
LABEL maintainer="rumble.travel <juan@rumble.travel>"
# Version 1.3

ARG GDAL_VERSION
ARG GEOS_VERSION
ARG PROJ_VERSION

ARG BUILD_TOOLS="build-essential file pkg-config wget"

USER root

# Fetch & install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends ${BUILD_TOOLS} dpkg sqlite3 libsqlite3-dev tar tzdata \
# Set timestamp post deps install
    && sleep 2 \
    && echo $(date --rfc-3339=seconds) > ./started_at \
# Install GEOS from source
    && mkdir cache_geos \
    && cd cache_geos \
    && wget https://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 \
    && tar xjf geos-${GEOS_VERSION}.tar.bz2 \
    && cd geos-${GEOS_VERSION} \
    && ./configure \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && ldconfig \
    && cd ../.. \
    && rm -r cache_geos \
#
# Install Proj4 from source
    && mkdir cache_proj \
    && cd cache_proj \
    && wget https://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz \
    && wget https://download.osgeo.org/proj/proj-datumgrid-latest.tar.gz \
    && tar xzf proj-${PROJ_VERSION}.tar.gz \
    && cd proj-${PROJ_VERSION} \
    && mkdir nad \
    && cd nad \
    && tar xzf ../../proj-datumgrid-latest.tar.gz \
    && cd .. \
    && ./configure \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && ldconfig \
    && cd ../.. \
    && rm -r cache_proj \
#
# Install GDAL from source
    && mkdir cache_gdal \
    && cd cache_gdal \
    && wget https://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz \
    && tar xzf gdal-${GDAL_VERSION}.tar.gz \
    && cd gdal-${GDAL_VERSION} \
    && ./configure --with-proj=/usr/local \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && ldconfig \
    && cd ../.. \
    && rm -r cache_gdal \
#
# libturbojpeg.so is not used by GDAL. Only libjpeg.so*
    && rm -f /usr/lib/libturbojpeg.so* \
# Only libwebp.so is used by GDAL
    && rm -f /usr/lib/libwebpmux.so* /usr/lib/libwebpdemux.so* /usr/lib/libwebpdecoder.so* \
# Cleanup uneccesary libgdal
    && rm -f /usr/local/lib/libgdal.a \
# Cleanup packages from earlier install
#    && apt-get purge -y --auto-remove ${BUILD_TOOLS} \
# Delete apt-get results
#    && rm -rf /var/lib/apt/lists/* \
#
# Package newly modified files in /usr/local with symlinks
    && tar --ignore-failed-read --newer-mtime="$(cat ./started_at)" -zcvf usrlocal.tar.gz -C /usr/local .; exit 0

# Create a minimum viable runner for Production
FROM ${BASE_IMAGE} as runner

USER root

COPY --from=builder /usrlocal.tar.gz /usrlocal.tar.gz

RUN tar -xvf /usrlocal.tar.gz -C /usr/local \
    && rm -rf /usrlocal.tar.gz
    && pip install --upgrade pip setuptools

ENV LD_LIBRARY_PATH="/lib:/usr/lib:/usr/local/lib:${LD_LIBRARY_PATH}"

CMD python3 -V && pip -V && gdalinfo --version && geos-config --version
