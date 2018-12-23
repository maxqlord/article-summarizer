from bs4 import BeautifulSoup
import requests

def return_page_content(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html5lib")
	all_text = []
	for paragraph in soup.findAll("p"):
		if len(paragraph.text) > 0:
			all_text.append(paragraph.text)

	return all_text



