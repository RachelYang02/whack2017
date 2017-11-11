"""
Feedback object
"""

class Feedback(object):

	def __init__(self, sentiment, ownership, passivity, overused_words):
		self.sentiment = convert_sentiment(sentiment)
		self.ownership = convert_ownnership(ownership)
		self.passivity = convert_passivity(passivity)
		self.overused_words = convert_overused_words(overused_words)

	def convert_sentiment(self, sentiment):
		if sentiment < .25:
			return "very negatively" #you spoke very negatively
		if sentiment < .5:
			return "negatively"
		if sentiment < .75:
			return "positively"
		return "very positively"

	def convert_ownnership(self, ownership):
		if ownership < .25:
			return "did not take ownership" #you did not take ownership
		if ownership < .5:
			return "did not take much ownership"
		if ownership < .75:
			return "took ownership"
		return "took a lot of ownership"

	def convert_passivity(self, passivity):
		if passivity < .25:
			return "very little" #you spoke very passively
		if passivity < .5:
			return "a little"
		if passivity < .75:
			return "very"
		return "far too"	

	def convert_overused_words(self, overused_words):
		word_string = ""
		for word in overused_words:
			word_string += word + ", "
		return word_string[0:-2] 	

	def give_feedback():
		text = "%s %s %s %s" % (self.sentiment, self.ownership, self.passivity, self.overused_words)
		return text