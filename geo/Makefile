GDAL_VERSION ?= 3.1.4
GEOS_VERSION ?= 3.8.1
PROJ_VERSION ?= 6.3.2
SPATIALITE_VERSION ?= 4.3.0a-5+b2

BASE_PYTHON_VERSION ?= 3.8.6
BASE_SOURCE_SUFFIX ?= slim-buster
BASE_IMAGE ?= python:$(BASE_PYTHON_VERSION)-$(BASE_SOURCE_SUFFIX)
IMAGE ?= rumbletravel/python-geodjango:py-$(BASE_PYTHON_VERSION)--gdal-$(GDAL_VERSION)--base-$(BASE_SOURCE_SUFFIX)

CI_PYTHON_VERSION ?= 3.8.6
CI_BASE_SOURCE_SUFFIX ?= circleci
CI_BASE_IMAGE ?= circleci/python:$(CI_PYTHON_VERSION)
CI_IMAGE ?= rumbletravel/python-geodjango:py-$(CI_PYTHON_VERSION)--gdal-$(GDAL_VERSION)--base-$(CI_BASE_SOURCE_SUFFIX)

image:
	docker build \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		--build-arg GDAL_VERSION=$(GDAL_VERSION) \
		--build-arg GEOS_VERSION=$(GEOS_VERSION) \
		--build-arg PROJ_VERSION=$(PROJ_VERSION) \
		--build-arg SPATIALITE_VERSION=$(SPATIALITE_VERSION) \
		-t $(IMAGE) .

image-ci:
	docker build \
		--build-arg BASE_IMAGE=$(CI_BASE_IMAGE) \
		--build-arg GDAL_VERSION=$(GDAL_VERSION) \
		--build-arg GEOS_VERSION=$(GEOS_VERSION) \
		--build-arg PROJ_VERSION=$(PROJ_VERSION) \
		--build-arg SPATIALITE_VERSION=$(SPATIALITE_VERSION) \
		-t $(CI_IMAGE) .

test:
	docker run $(IMAGE)

test-ci:
	docker run $(CI_IMAGE)

push-image:
	docker push $(IMAGE)

push-image-ci:
	docker push $(CI_IMAGE)

.PHONY: image test push-image
