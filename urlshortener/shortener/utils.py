import random, string, requests, urllib2
from bs4 import BeautifulSoup
from .models import PageURL

def generate_url_id(length=6):
	sys_random = random.SystemRandom()
	while True:
		url_id = ''.join(
	            sys_random.sample(string.ascii_lowercase + string.ascii_uppercase, length)
	            )
		try:
			checkurl = PageURL.objects.get(url_id=url_id)
		except:
			return url_id

def scrape_data(long_url):
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(long_url, headers=hdr)
	response = urllib2.urlopen(req)
	soup = BeautifulSoup(response, 'html.parser')
	try:
		title = soup.title.string
	except:
		title = "Bez tytulu"
	# try:
	# 	description = soup.find(attrs={'name': 'Description'})
	# 	# if description == None:
	# 	# 	description = soup.find(attrs={'name': 'description'})
	# except:
	# 	description = "Brak opisu"
	return {
			"title": title.encode("utf-8"), 
			"description": "brak opisu",
			}

