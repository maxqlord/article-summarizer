from bs4 import BeautifulSoup
import requests

class ArticleScraper():

	def __init__(self, url, html_scraper="html5lib"):
		self.url = url
		self.html_scraper = html_scraper

	def return_page_content(self):
		r = requests.get(self.url)
		soup = BeautifulSoup(r.content, self.html_scraper)
		all_text = []
		for paragraph in soup.findAll("p"):
			if len(paragraph.text) > 0:
				all_text.append(paragraph.text)
		print(all_text)
		return all_text

	def split_by_sentences(self,all_text):
		#TODO Include issues like N.F.L. ,  Dr. ,  Jan. 1 , U.S. , middle initials, include quote if after period
		period = "."
		sentence_list = []
		honorifics_len_2 = ["mr", "ms", "dr"]
		honorifics_len_3 = ["mrs", "esq"]
		for paragraph in all_text:
			if period in paragraph:  #Actual sentence
				last_period_index = -1
				for char_index in range(len(paragraph)):
					if paragraph[char_index] == "." and char_index > 1:
						if paragraph[char_index-2: char_index].lower() not in honorifics_len_2 and \
						paragraph[char_index-3: char_index].lower() not in honorifics_len_3:

							sentence_list.append(paragraph[last_period_index + 1:char_index + 1])
							last_period_index = char_index
		print(sentence_list)
		return sentence_list

	def scrape(self):
		return split_by_sentences(return_page_content())