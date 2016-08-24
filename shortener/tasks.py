# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

from celery import shared_task


@shared_task
def scrape_data(long_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(long_url, headers=hdr)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    try:
        title = soup.title.string
    except:
        title = "No title"

    # currently not scraping any description
    # many websites have no meta-description tag
    # we can replace this with e.g. scraping content of first <p> tag
    return {
        "title": title.encode("utf-8"),
        "description": "No description",
    }
