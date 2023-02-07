NAME=indeed-webscraper
REPO_NAME = $(NAME)
WORKDIR = $(shell pwd)
PYTHONPATH:= $(PYTHONPATH):$(WORKDIR)/indeed-scraper
DOT_ENV = $(WORKDIR)/.env
DOCKER_DIR = $(WORKDIR)/docker
APP_DOCKER_FILE = $(DOCKER_DIR)/Dockerfile.app
DOCKER_PACKAGE = docker.pkg.github.com
IMAGE_NAME = $(REPO_NAME):latest
FULL_IMAGE_NAME = $(DOCKER_PACKAGE)/$(IMAGE_NAME)

build:
	docker build -t $(FULL_IMAGE_NAME) -f $(APP_DOCKER_FILE) .

push:
	docker tag $(IMAGE_NAME) $(FULL_IMAGE_NAME)
	docker push $(FULL_IMAGE_NAME)

push-image: build push

run:
	export PYTHONPATH=$(PYTHONPATH)
	streamlit run app/money_gun.py

scrapy:
	scrapy crawl indeed_jobs -o test.csv

include Makefile.venv