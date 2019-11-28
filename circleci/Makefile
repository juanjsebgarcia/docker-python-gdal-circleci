GDAL_VERSION ?= 2.3.3
PYTHON_VERSION ?= 3.7
BASE_SOURCE ?= circleci
BASE_IMAGE ?= $(BASE_SOURCE)/python:$(PYTHON_VERSION)
IMAGE ?= rumbletravel/python-gdal-circle:py$(PYTHON_VERSION)-gdal$(GDAL_VERSION)-base$(BASE_SOURCE)

image:
	docker build \
		--build-arg GDAL_VERSION=$(GDAL_VERSION) \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		-t $(IMAGE) .

test:
	docker run $(IMAGE)

lint:
	docker run \
		-v `pwd`/.dockerfilelintrc:/.dockerfilelintrc \
		-v `pwd`/Dockerfile:/Dockerfile \
		replicated/dockerfilelint /Dockerfile

push-image:
	docker push $(IMAGE)

.PHONY: image test lint push-image
