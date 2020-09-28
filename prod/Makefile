GDAL_VERSION ?= 3.1.2
PYTHON_VERSION ?= 3.8.5
BASE_SOURCE ?= slim-buster
IMAGE ?= rumbletravel/python-gdal-circle:py-$(PYTHON_VERSION)--gdal-$(GDAL_VERSION)--base-$(BASE_SOURCE)

image:
	docker build \
		-t $(IMAGE) .

test:
	docker run $(IMAGE)

push-image:
	docker push $(IMAGE)

.PHONY: image test push-image
