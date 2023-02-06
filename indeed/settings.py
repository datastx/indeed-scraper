import os
from dotenv import load_dotenv

load_dotenv(os.getenv('DOT_ENV'))  # take environment variables from .env.

if os.getenv('SRAPPY_SECRET',"") == "":
    raise ValueError('SRAPPY_SECRET is not set. Abort')
BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

## ScrapeOps API Key
SCRAPEOPS_API_KEY = os.getenv('SRAPPY_SECRET') ## Get Free API KEY here: https://scrapeops.io/app/register/main
## Enable ScrapeOps Proxy
SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}

## Insert Your List of Proxies Here
# ROTATING_PROXY_LIST = [
#     'proxy1.com:8000',
#     'proxy2.com:8031',
#     'proxy3.com:8032',
# ]


DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # Rotating Proxy Middleware
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    
    ## Proxy Middleware
    'indeed.middlewares.ScrapeOpsProxyMiddleware': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 15
