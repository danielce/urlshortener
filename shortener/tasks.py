# -*- coding: utf-8 -*-.
import urllib2
from bs4 import BeautifulSoup
from celery import shared_task

from django.utils.text import Truncator


@shared_task
def scrape_data(long_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(long_url, headers=hdr)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')

    title = soup.title.string

    meta_tags = soup.findAll('meta', {"property": 'og:description'})
    og_desc = meta_tags[0].get('content', 'No description')
    description = Truncator(og_desc).chars(200)

    return {
        "title": title.encode("utf-8"),
        "description": description.encode("utf-8"),
    }
