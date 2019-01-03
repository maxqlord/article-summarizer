from bs4 import BeautifulSoup
import requests
import string

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
				all_text.append(" " + paragraph.text)
		return all_text


	
	def split_by_sentences(self,all_text):
		#TODO Include issues like N.F.L. ,  Dr. ,  Jan. 1 , U.S. , middle initials, include quote if after period
		period = "."
		sentence_list = []
		honorifics_len_2 = ["mr", "ms", "dr"]
		honorifics_len_3 = ["mrs", "esq"]
		for paragraph in all_text:
			if period in paragraph and (paragraph[0].isupper() or paragraph[1].isupper()):  #Actual sentence
				last_period_index = -1
				for char_index in range(len(paragraph)):
					if paragraph[char_index] == period and char_index > 1:
						if paragraph[char_index-2: char_index].lower() not in honorifics_len_2 and \
						paragraph[char_index-3: char_index].lower() not in honorifics_len_3:

							sentence_list.append(paragraph[last_period_index + 1:char_index + 1])
							last_period_index = char_index
		return sentence_list

	def check_sentences(self, sentence_list):
		new_sentence_list = []
		after_strip = []
		triggered = False
		for sentence in sentence_list:
			if len(sentence) < 3:
				new_sentence_list[len(new_sentence_list)-1] += sentence
				triggered = True
			else:
				if triggered and (sentence[0].isupper() or sentence[0].isupper()):
					new_sentence_list[len(new_sentence_list)-1] += sentence
					triggered = False
				else:
					new_sentence_list.append(sentence.strip())

		for sentence in new_sentence_list:
			if len(after_strip) > 0:
				if sentence[0].isalpha() and sentence[0].islower():
					after_strip[len(after_strip)-1] = after_strip[len(after_strip)-1] + " " + sentence
				elif sentence[0] == "’":
					after_strip[len(after_strip)-1] = after_strip[len(after_strip)-1] + sentence
				else:
					after_strip.append(sentence)
			else:
				after_strip.append(sentence)

		for sentence in after_strip:
			print(sentence + "\n")
		return [sentence for sentence in after_strip if len(sentence.split()) > 4]
	
	def scrape(self):
		return self.check_sentences(self.split_by_sentences(self.return_page_content()))

#scraper = ArticleScraper("https://www.nytimes.com/2018/12/31/sports/nfl-black-coaches-fired.html")

