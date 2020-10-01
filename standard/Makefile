BASE_PYTHON_VERSION ?= 3.8.6
BASE_SOURCE_SUFFIX ?= slim-buster
BASE_IMAGE ?= python:$(BASE_PYTHON_VERSION)-$(BASE_SOURCE_SUFFIX)
IMAGE ?= rumbletravel/python:py-$(BASE_PYTHON_VERSION)--base-$(BASE_SOURCE_SUFFIX)

CI_PYTHON_VERSION ?= 3.8.6
CI_BASE_SOURCE_SUFFIX ?= circleci
CI_BASE_IMAGE ?= circleci/python:$(CI_PYTHON_VERSION)
CI_IMAGE ?= rumbletravel/python:py-$(CI_PYTHON_VERSION)--base-$(CI_BASE_SOURCE_SUFFIX)

image:
	docker build \
		--build-arg BASE_IMAGE=$(BASE_IMAGE) \
		-t $(IMAGE) .

image-ci:
	docker build \
		--build-arg BASE_IMAGE=$(CI_BASE_IMAGE) \
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
