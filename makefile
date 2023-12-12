DOCKER_REPOSITORY := labeling_ground/api_server

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml
IMAGE_VERSION := 1.0.0

PREDICTION_CACHE_PATTERN := sam
PREDICTION_CACHE_PATTERN_PREP := proxy
PREDICTION_CACHE_PATTERN_PREP_PORT := 8000
SEGMENT_DOCKER_GPU_REPOSITORY := sam-gpu
SEGMENT_DOCKER_CPU_REPOSITORY := sam-cpu
SEGMENT_DOCKER_PATH := segment_anything


.PHONY: build_proxy
build_proxy:
	docker build \
		-t $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION) \
		-f ./$(DOCKERFILE).proxy .

.PHONY: push_proxy
push_proxy:
	docker push $(DOCKER_REPOSITORY):$(PREDICTION_CACHE_PATTERN)_$(PREDICTION_CACHE_PATTERN_PREP)_$(IMAGE_VERSION)

.PHONY: build_gpu
build_gpu:
	docker build \
		-t $(SEGMENT_DOCKER_GPU_REPOSITORY):$(IMAGE_VERSION) \
		-f ./$(SEGMENT_DOCKER_PATH)/$(DOCKERFILE)-gpu .

.PHONY: push_gpu
push_gpu:
	docker push $(SEGMENT_DOCKER_GPU_REPOSITORY):$(IMAGE_VERSION)

.PHONY: build_cpu
build_cpu:
	docker build \
		-t $(SEGMENT_DOCKER_CPU_REPOSITORY):$(IMAGE_VERSION) \
		-f ./$(SEGMENT_DOCKER_PATH)/$(DOCKERFILE)-cpu .

.PHONY: build_all
build_all: build_proxy build_gpu build_cpu

.PHONY: push_all
push_all: push_proxy build_gpu build_cpu

.PHONY: c_build
c_build: build_all

.PHONY: c_up
c_up:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		up -d

.PHONY: c_down
c_down:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		down