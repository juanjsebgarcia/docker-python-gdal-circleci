FROM python:3.7.5-alpine3.10 as builder
MAINTAINER rumble.travel <juan@rumble.travel>
# Version 1.0

# Inspired by OSGeo/gdal by Even Rouault
# https://github.com/OSGeo/gdal/blob/master/gdal/docker/alpine-small/Dockerfile
ARG BUILD_TOOLS="wget curl unzip make libtool autoconf automake pkgconfig g++ sqlite sqlite-dev alpine-sdk linux-headers"


# Fetch & install dependencies
RUN apk add --no-cache --update-cache ${BUILD_TOOLS}
RUN apk add --no-cache \
    curl-dev \
    zlib-dev zstd-dev \
    libjpeg-turbo-dev libpng-dev libwebp-dev expat-dev postgresql-dev openjpeg


# Install Proj4 datumgrid
RUN mkdir -p /build_projgrids/usr/share/proj \
    && curl -LOs http://download.osgeo.org/proj/proj-datumgrid-latest.zip \
    && unzip -q -j -u -o proj-datumgrid-latest.zip  -d /build_projgrids/usr/share/proj \
    && rm -f *.zip


# Build PROJ
RUN mkdir proj \
    && wget -q https://github.com/OSGeo/proj.4/archive/5.2.0.tar.gz -O - \
        | tar xz -C proj --strip-components=1 \
    && cd proj \
    && ./autogen.sh \
    && ./configure --prefix=/usr --disable-static --enable-lto \
    && make -j$(nproc) \
    && make -j$(nproc) install \
    && make -j$(nproc) install DESTDIR="/build_proj" \
    && cd .. \
    && rm -rf proj \
    && for i in /build_proj/usr/lib/*; do strip -s $i 2>/dev/null || /bin/true; done \
    && for i in /build_proj/usr/bin/*; do strip -s $i 2>/dev/null || /bin/true; done


# Install GEOS from source
RUN mkdir cache_geos \
    && cd cache_geos \
    && wget https://download.osgeo.org/geos/geos-3.7.3.tar.bz2 \
    && tar xjf geos-3.7.3.tar.bz2 \
    && cd geos-3.7.3 \
    && ./configure \
    && make -j"$(nproc)" \
    && make -j"$(nproc)" install \
    && cd ../.. \
    && rm -r cache_geos


RUN apk add --no-cache --update-cache tar
# Install GDAL from source
RUN mkdir gdal \
    && wget -q https://github.com/OSGeo/gdal/archive/v2.3.3.tar.gz -O - \
        | tar xz -C gdal --strip-components=1 \
    && cd gdal/gdal \
    && ./configure --prefix=/usr --without-libtool \
    --with-hide-internal-symbols \
    --with-proj=/usr \
    --with-libtiff=internal --with-rename-internal-libtiff-symbols \
    --with-geotiff=internal --with-rename-internal-libgeotiff-symbols \
    --enable-lto \
    && make -j$(nproc) \
    && make -j$(nproc) install DESTDIR="/build" \
    && cd ../.. \
    && rm -rf gdal \
    && mkdir -p /build_gdal_version_changing/usr/include \
    && mv /build/usr/lib                    /build_gdal_version_changing/usr \
    && mv /build/usr/include/gdal_version.h /build_gdal_version_changing/usr/include \
    && mv /build/usr/bin                    /build_gdal_version_changing/usr \
    && for i in /build_gdal_version_changing/usr/lib/*; do strip -s $i 2>/dev/null || /bin/true; done \
    && for i in /build_gdal_version_changing/usr/bin/*; do strip -s $i 2>/dev/null || /bin/true; done \
    # Remove resource files of uncompiled drivers
    && (for i in \
            # BAG driver
            /build/usr/share/gdal/bag*.xml \
            # unused
            /build/usr/share/gdal/*.svg \
            # unused
            /build/usr/share/gdal/*.png \
            # GMLAS driver
            /build/usr/share/gdal/gmlas* \
            # netCDF driver
            /build/usr/share/gdal/netcdf_config.xsd \
       ;do rm $i; done)

# Cleanup
RUN apk del --no-cache ${BUILD_TOOLS} \
        && rm -rf /var/lib/apt/lists/* \
        && rm -rf /var/cache/apt/* \

# Misc
## Reinstall just uninstalled Django requirement
        && apk add --no-cache binutils

CMD python3 -V && pip -V && gdalinfo --version && geos-config --version

# Build final image
FROM python:3.7.5-alpine3.10 as runner

COPY --from=builder  /build_projgrids/usr/ /usr/

COPY --from=builder  /build_proj/usr/share/proj/ /usr/share/proj/
COPY --from=builder  /build_proj/usr/include/ /usr/include/
COPY --from=builder  /build_proj/usr/bin/ /usr/bin/
COPY --from=builder  /build_proj/usr/lib/ /usr/lib/

COPY --from=builder  /build/usr/share/gdal/ /usr/share/gdal/
COPY --from=builder  /build/usr/include/ /usr/include/
COPY --from=builder  /build_gdal_version_changing/usr/ /usr/

RUN apk add --no-cache --update-cache \
        alpine-sdk \
        openssl-dev \
        libffi-dev \
        libstdc++ \
        postgresql-dev \
        sqlite-libs \
        libcurl \
        zlib zstd-libs\
        libjpeg-turbo libpng openjpeg libwebp expat libpq \
    && apk add --no-cache --update-cache \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
        geos \
    # libturbojpeg.so is not used by GDAL. Only libjpeg.so*
    && rm -f /usr/lib/libturbojpeg.so* \
    # Only libwebp.so is used by GDAL
    && rm -f /usr/lib/libwebpmux.so* /usr/lib/libwebpdemux.so* /usr/lib/libwebpdecoder.so* \

# Install latest Numpy
    && pip install numpy \

# Install Python GDAL
    && pip install --upgrade pip \
    && pip install GDAL==2.3.3
