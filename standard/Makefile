BASE_PYTHON_VERSION ?= 3.8.6
BASE_SOURCE_SUFFIX ?= slim-buster
BASE_IMAGE ?= python:$(BASE_PYTHON_VERSION)-$(BASE_SOURCE_SUFFIX)
IMAGE ?= rumbletravel/python:py-$(BASE_PYTHON_VERSION)--base-$(BASE_SOURCE_SUFFIX)

image:
	docker build \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		-t $(IMAGE) .

test:
	docker run $(IMAGE)

push-image:
	docker push $(IMAGE)

.PHONY: image test push-image
