NAME=indeed-webscraper
WORKDIR = $(shell pwd)
PYTHONPATH:= $(PYTHONPATH):$(WORKDIR)/indeed-scraper
DOT_ENV = $(WORKDIR)/.env

run:
	export PYTHONPATH=$(PYTHONPATH)
	streamlit run app/money_gun.py

scrapy:
	scrapy crawl indeed_jobs -o test.csv

include Makefile.venv