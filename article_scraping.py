from bs4 import BeautifulSoup
import requests
import common_words
from math import log10
from collections import OrderedDict
from operator import itemgetter

class ArticleScraper():

	def __init__(self, url, html_scraper="html5lib"):
		self.url = url
		self.html_scraper = html_scraper
		self.word_count = {}
		self.common = common_words.common.split()

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
			if period in paragraph and (char.isupper() for char in paragraph[:5]):  #Actual sentence
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
				if triggered and (sentence[0].isalnum()):
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
		
		return [sentence for sentence in after_strip if len(sentence.split()) > 4]

	def count_words(self, sentence_list):
		for sentence in sentence_list:
			for word in sentence.split():
				word.replace('.', '')
				if word in self.word_count and word not in self.common:
					self.word_count[word] += 1
				else:
					self.word_count[word] = 1

	def score_sentences(self, sentence_list):
		top_sentences = {}
		for sentence_index in range(len(sentence_list)):
			score = 0
			words_in_sentence = 0
			for word in sentence_list[sentence_index].split():
				word.replace('.', '')
				if word in self.word_count:
					score += self.word_count[word]
					words_in_sentence += 1
			top_sentences[sentence_index] = self.scaled_score(score, words_in_sentence)
		top_index_dict = OrderedDict(sorted(top_sentences.items(), key=itemgetter(1), reverse=True))
		return [sentence_list[index] for index in list(top_index_dict.keys())[:5]]

	def scaled_score(self, score, words_in_sentence):
		length_multiplier = 1/(3*log10(words_in_sentence))
		return score*length_multiplier

	def scrape(self):
		content = self.return_page_content()
		sentences = self.check_sentences(self.split_by_sentences(content))
		self.count_words(sentences)
		sentence_rank = self.score_sentences(sentences)
		print(' '.join(sentence_rank))

def main():
	input_link = input("Enter article link to summarize: ")
	scraper = ArticleScraper("https://www.nytimes.com/2018/12/31/sports/nfl-black-coaches-fired.html")
	if input_link: 
		scraper = ArticleScraper(input_link)
	scraper.scrape()

main()
