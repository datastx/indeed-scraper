NAME=indeed-webscraper
WORKDIR = $(shell pwd)
PYTHONPATH:= $(PYTHONPATH):$(WORKDIR)/indeed-scraper
DOT_ENV = $(WORKDIR)/.env
VENV_DIR = $(WORKDIR)/.venv
VENV_BIN = $(VENV_DIR)/bin
DOCKER_FILES = $(WORKDIR)/docker
POSTGRES_CONTAINER_NAME=heroes-pg
POSTGRES_IMAGE_NAME=local-pg-build
POSTGRES_PORT=5432
POSTGRES_DOCKER_FILE = $(DOCKER_FILES)/Dockerfile.postgres


run:
	export PYTHONPATH=$(PYTHONPATH)
	streamlit run app/money_gun.py

scrapy:
	scrapy crawl indeed_jobs -o test.csv

include Makefile.venv