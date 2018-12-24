from bs4 import BeautifulSoup
import requests

def return_page_content(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html5lib")
	all_text = []
	for paragraph in soup.findAll("p"):
		if len(paragraph.text) > 0:
			all_text.append(paragraph.text)
	print(all_text)
	return all_text

def split_by_sentences(all_text):
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

split_by_sentences(return_page_content("https://www.nytimes.com/2018/12/23/us/politics/trump-mattis.html"))