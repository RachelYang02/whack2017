"""
Whack 2017 Alexa
Hour 1
Text Analysis for Length, 
Speed, and Sentiment.
"""

import indicoio
import time
import re
indicoio.config.api_key = '7b7ddd4e3120df54b1a4018d77e01f9c'

f = open('pride.txt','r')
test_paragraph = f.read()

# Sentiment
def sentiment_analysis(string):
	return indicoio.sentiment(string)
print sentiment_analysis(test_paragraph)


# Length
# helper functions
def time_to_s(minute):
	return minute * 60

def time_to_m(second):
	return second / 60
# main
def length_analysis(string):
	start_time = time.time()
	f = open('pride.txt', 'r')
	end_time = time.time()

	return end_time - start_time

print time_to_m(length_analysis(test_paragraph))


# Speed
def speed_analysis(string):
	passage = []
	parsed_string = re.sub(r'[^\w\s]','',string)	
	passage = parsed_string.split(" ")
	return length_analysis(string) / len(passage)
	
print speed_analysis(test_paragraph)

