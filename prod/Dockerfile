FROM python:3.8.5-slim-buster as builder
MAINTAINER rumble.travel <juan@rumble.travel>
# Version 1.1

ARG BUILD_TOOLS="build-essential file pkg-config wget"

# Fetch & install dependencies
RUN echo $(date --rfc-3339=seconds) > ./started_at \
    && apt-get update \
    && apt-get install -y --no-install-recommends ${BUILD_TOOLS} sqlite3 libsqlite3-dev \

# Install GEOS from source
    && mkdir cache_geos \
    && cd cache_geos \
    && wget https://download.osgeo.org/geos/geos-3.8.1.tar.bz2 \
    && tar xjf geos-3.8.1.tar.bz2 \
    && cd geos-3.8.1 \
    && ./configure \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && ldconfig \
    && cd ../.. \
    && rm -r cache_geos \

# Install Proj4 from source
    && mkdir cache_proj \
    && cd cache_proj \
    && wget https://download.osgeo.org/proj/proj-6.3.1.tar.gz \
    && wget https://download.osgeo.org/proj/proj-datumgrid-latest.tar.gz \
    && tar xzf proj-6.3.1.tar.gz \
    && cd proj-6.3.1 \
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

# Install GDAL from source
    && mkdir cache_gdal \
    && cd cache_gdal \
    && wget https://download.osgeo.org/gdal/3.1.2/gdal-3.1.2.tar.gz \
    && tar xzf gdal-3.1.2.tar.gz \
    && cd gdal-3.1.2 \
    && ./configure --with-proj=/usr/local \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && ldconfig \
    && cd ../.. \
    && rm -r cache_gdal \

    && pip install --upgrade pip setuptools \

# libturbojpeg.so is not used by GDAL. Only libjpeg.so*
    && rm -f /usr/lib/libturbojpeg.so* \
# Only libwebp.so is used by GDAL
    && rm -f /usr/lib/libwebpmux.so* /usr/lib/libwebpdemux.so* /usr/lib/libwebpdecoder.so* \
# Cleanup uneccesary libgdal
    && rm -f /usr/local/lib/libgdal.a \
# Cleanup packages from earlier install
    && apt-get purge -y --auto-remove ${BUILD_TOOLS} \

# Package newly modified files in /usr/local with symlinks
    && tar --newer-mtime="$(cat ./started_at)" -zcvf usrlocal.tar.gz -C /usr/local .



# Create a minimum viable runner for Production
FROM python:3.8.5-slim-buster

COPY --from=builder /usrlocal.tar.gz /usrlocal.tar.gz
RUN tar -xvf /usrlocal.tar.gz -C /usr/local \
    && rm -rf /usrlocal.tar.gz

ENV LD_LIBRARY_PATH="/lib:/usr/lib:/usr/local/lib:${LD_LIBRARY_PATH}"

CMD python3 -V && pip -V && gdalinfo --version && geos-config --version
