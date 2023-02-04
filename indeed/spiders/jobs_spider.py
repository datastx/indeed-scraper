import json
import os
import re
from urllib.parse import urlencode
import pdb
import logging
import scrapy


class IndeedJobSpider(scrapy.Spider):
    name = "indeed_jobs"

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {
            "q": keyword,
            "l": location,
            "sort": "date",
            "filter": 0,
            "start": offset,
        }
        url = "https://www.indeed.com/jobs?" + urlencode(parameters)
        logging.info(f"requesting url:{url}")
        return url

    def start_requests(self):
        keyword_list = [os.environ.get("WHAT", None)]
        location_list = [os.environ.get("WHERE", None)]
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_search_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(
                    url=indeed_jobs_search_url,
                    callback=self.count_total_jobs_in_search,
                    meta={
                        "keyword": keyword,
                        "location": location,
                        "offset": 0,
                    },
                )

    def count_total_jobs_in_search(self, response):
        location = response.meta["location"]
        keyword = response.meta["keyword"]
        offset = response.meta["offset"]
        script_tag = re.findall(
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
            response.text,
        )
        if script_tag is not None:
            pattern = re.compile(r'"totalJobCount":([\d,]+)')
            match = re.search(pattern, response.text)
            num_results = int(match.group(1).replace(",", ""))
            # We want this to error if not set
            start_page = int(os.getenv('START_PAGE',None))
            end_page = int(os.getenv('END_PAGE',None))
            for index, _ in enumerate(range(0, num_results, 15)):
                if start_page <= index + 1 < end_page:
                    if index == 0:
                        offset = 0
                    else:
                        offset = index * 10
                    url = self.get_indeed_search_url(keyword, location, offset)

                    yield scrapy.Request(
                        url=url,
                        callback=self.submit_jobs_per_page,
                        dont_filter=True,
                        meta={
                            "keyword": keyword,
                            "location": location,
                            "offset": offset,
                            "indeed_jobs_search_url": url,
                            "num_results": num_results,
                            "page": index + 1,
                        },
                    )

    def submit_jobs_per_page(self, response):
        location = response.meta["location"]
        keyword = response.meta["keyword"]

        indeed_jobs_search_url = response.meta["indeed_jobs_search_url"]
        num_results = response.meta["num_results"]
        page = response.meta["page"]
        script_tag = re.findall(
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
            response.text,
        )
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])

            ## Extract Jobs From Search Page
            jobs_list = json_blob["metaData"]["mosaicProviderJobCardsModel"]["results"]

            for index, job in enumerate(jobs_list, 0):
                if job.get("jobkey") is not None:
                    indeed_job_url = (
                        "https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk="
                        + job.get("jobkey")
                    )
                    yield scrapy.Request(
                        url=indeed_job_url,
                        callback=self.parse_job,
                        meta={
                            "keyword": keyword,
                            "location": location,
                            "page": page,
                            "position": index,
                            "jobKey": job.get("jobkey"),
                            "indeed_jobs_search_url": indeed_jobs_search_url,
                            "indeed_job_url": indeed_job_url,
                            "num_results": num_results,
                        },
                    )

    def parse_job(self, response):
        location = response.meta["location"]
        keyword = response.meta["keyword"]
        page = response.meta["page"]
        position = response.meta["position"]
        indeed_jobs_search_url = response.meta["indeed_jobs_search_url"]
        indeed_job_url = response.meta["indeed_job_url"]
        num_results = response.meta["num_results"]

        script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
            yield {
                "keyword": keyword,
                "location": location,
                "page": page,
                "position": position,
                "company": job.get("jobInfoHeaderModel", {}).get("companyName"),
                "jobkey": response.meta["jobKey"],
                "jobTitle": job.get("jobInfoHeaderModel", {}).get("jobTitle"),
                "jobDescription": job.get("sanitizedJobDescription").get("content")
                if job.get("sanitizedJobDescription") is not None
                else "",
                "indeed_jobs_search_url": indeed_jobs_search_url,
                "indeed_job_url": indeed_job_url,
                "num_results": num_results,
            }
