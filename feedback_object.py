"""
Feedback object -- might make sense for calculations to go here too
"""
import indicoio
import time
import re
indicoio.config.api_key = '7b7ddd4e3120df54b1a4018d77e01f9c'

class Feedback(object):

	def __init__(self, text):
		word_dict, total_words = word_freq(text)
		raw_sentiment = sentiment_analysis(text)
		raw_ownership = ownership_measure(word_dict)
		raw_overused_words = overused_words(word_dict, total_words)
		raw_passivity = passive_analysis(text)

		self.sentiment = convert_sentiment(raw_sentiment)
		self.ownership = convert_ownnership(raw_ownership)
		self.passivity = convert_passivity(raw_passivity)
		self.overused_words = convert_overused_words(raw_overused_words)

	def convert_sentiment(self, sentiment):
		if sentiment < .5:
			return "negatively. Try and keep your answers hopeful and focus the positive outcomes of experiences."
		return "positively. People probably feel that you would bring a positive presence to the company."

	def convert_ownnership(self, ownership):
		if ownership < .3:
			return "You said we very often, which discounts your role in projects and teams. Try using the active I more to claim ownership of what you have done"
		if ownership < .7:
			return "You almost always took ownership. You emphasized your role, but still attributed your accomplishments to others occasionally."
		return "You always took ownership! It was clear what your contributions were and the impact you had"

	def convert_passivity(self, passivity):
		if passivity < .3:
			return "You rarely used the passive voice. It made it seem like you were confident about what you were saying."
		return "You often used the passive voice. Attempting to use the active voice will make you sound more confident."	

	def convert_overused_words(self, overused_words):
		if len(overused_words) == 0:
			word_string = "The words you said most include "
			for n in range(len(overused_words) - 1):
				word_string += overused_words[n] + ", "
			word_string += "and " + overused_words[-1] + "."
			return word_string
		else:
			return "You did not have many repeated words in your answers. Good job!"

	def give_feedback():
		start = "Lets talk about how that went. I scored your interview based on a few metrics, including the length of your answers, how often you used passive voice, how often you used certain words, how fast you were speaking, how positive or negative you seemed, and finally how often you took ownership of projects. Each of these areas are traditionally where women are weaker than their male counterparts. "
		ownership = " Lets move on to your use of I vs We pronouns. In interviews, you want to make it clear that you are the one at the center of your experiences - interviewers do not care about your teammates accomplishments. " + self.ownership
		passivity = " Using the passive voice instead of the active voice can make it seem as if you are not confident about what you are saying. " + self.passivity
		sentiment = " It’s important to understand how positive or negative people might see you. In this interview, you came across as " + self.sentiment
		overuse = " Repeating words can emphasize points, but also become distracting. " + self.overused_words
		end = "If you would like to see your detailed results, please visit the website PANTSUITUP.ORG. Thank you for practicing with me today. If you wish to practice again, say XXXX. Otherwise, good luck!"
		text = start + ownership + passivity + sentiment + overuse + end
		return text


	"""**************** CALCULATION FUNCTIONS BELOW ****************"""

	def sentiment_analysis(text):
		"""
		Uses Indico Sentiment Analysis API to find postivity-negativity value of text
		"""
		return indicoio.sentiment(text)

	def word_freq(text):
		"""
		Creates and returns a dictionary of words mapped to their frequencies as well as the total number of words
		"""
		word_dict = dict()
		text_wo_punc = text.translate(None, string.punctuation)

		# download nltk packages first time running program
		try:
			word_list = nltk.pos_tag(nltk.word_tokenize(text_wo_punc))
		except:
			nltk.download('punkt')
			nltk.download('averaged_perceptron_tagger')
			word_list = nltk.pos_tag(nltk.word_tokenize(text_wo_punc))

		for word, pos in word_list:
			if word in word_dict:
				word_dict[word] += 1
			elif pos != 'CC' and pos != 'IN' and pos != 'TO' and pos != 'DT': # exclude prepositions, conjunctions, etc
				word_dict[word] = 1

		return word_dict, len(word_list)

	def ownership_measure(word_dict):
		""" 
		Calculates and returns measure of ownership as judged by frequency of first_person vs second_person pronouns used
		"""
		first_person = 0
		second_person = 0

		if "I" in word_dict:
			first_person += word_dict["I"]
		if "me" in word_dict:
			first_person += word_dict["me"]
		if "my" in word_dict:
			first_person += word_dict["my"]
		if "we" in word_dict:
			second_person += word_dict["we"]
		if "us" in word_dict:
			second_person += word_dict["us"]
		if "our" in word_dict:
			second_person += word_dict["our"]

		return (float(first_person) / (second_person + first_person))

	def passive_analysis(text):
		"""
		Measures proportion of passive sentences to all sentences
		"""
		passive_voice = {'passive': 0}
		passive_verb = ['is','are','am','was','were','had','has','have']
		passage_sent = re.split('(?<=[.!?]) +',text)
		for sent in passage_sent:
			passage_word_sent = sent.split(" ")
			for i, word in enumerate(passage_word_sent):
				if word in passive_verb:
					if (passage_word_sent[i+1][-3:] == 'ing') or (passage_word_sent[i+1][-2:] == 'en') or (passage_word_sent[i+1][-2:] == 'ed'):
						passive_voice['passive'] += 1

		return passive_voice['passive'] / float(len(passage_sent))

	def overused_words(word_dict, total_words):
		""" 
		Finds words that makes up more than 1% of a person's answers and returns them as a list of overused words
		"""
		overused_words_list = []
		
		if total_words > 500:
			threshold = .01
		else:
			threshold = .05
		
		for word, count in word_dict.iteritems():
			if (count / float(total_words)) > threshold: 
				overused_words_list.append(word)

		return overused_words_list