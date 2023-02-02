NAME=indeed-webscraper
WORKDIR = $(shell pwd)
DOT_ENV = $(WORKDIR)/.env
VENV_DIR = $(WORKDIR)/.venv
VENV_BIN = $(VENV_DIR)/bin
DOCKER_FILES = $(WORKDIR)/docker
POSTGRES_CONTAINER_NAME=heroes-pg
POSTGRES_IMAGE_NAME=local-pg-build
POSTGRES_PORT=5432
POSTGRES_DOCKER_FILE = $(DOCKER_FILES)/Dockerfile.postgres


run:
	streamlit run app/main.py

scrapy:
	export DOT_ENV=$(DOT_ENV) 
	scrapy crawl indeed_jobs -o indeed_jobs_data.csv

include Makefile.venv