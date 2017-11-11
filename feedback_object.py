"""
Feedback object -- might make sense for calculations to go here too
"""

class Feedback(object):

	def __init__(self, sentiment, ownership, passivity, overused_words):
		self.sentiment = convert_sentiment(sentiment)
		self.ownership = convert_ownnership(ownership)
		self.passivity = convert_passivity(passivity)
		self.overused_words = convert_overused_words(overused_words)

	def convert_sentiment(self, sentiment):
		if sentiment < .3:
			return "very negatively" #you spoke very negatively
		if sentiment < .7:
			return "negatively"
		return "very positively"

	def convert_ownnership(self, ownership):
		if ownership < .3:
			return "You said we very often, which discounts your role in projects and teams. Try using the active ‘I’ more to claim ownership of what you’ve done"
		if ownership < .7:
			return "You almost always took ownership. You emphasized your role, but still attributed your accomplishments to others occasionally."
		return "You always took ownership! It was clear what your contributions were and the impact you had"

	def convert_passivity(self, passivity):
		if passivity < .3:
			return "very little" #you spoke very passively
		if passivity < .7:
			return "a little"
		return "far too"	

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
		start = "Let’s talk about how that went. I scored your interview based on a few metrics, including the length of your answers, how often you used passive voice, how often you used certain words, how fast you were speaking, how positive or negative you seemed, and finally how often you took ownership of projects. Each of these areas are traditionally where women are weaker than their male counterparts. "
		ownership = " Let’s move on to your use of I vs We pronouns. In interviews, you want to make it clear that you are the one at the center of your experiences - interviewers do not care about your teammates’ accomplishments. " + self.ownership
		passivity = " Using the passive voice instead of the active voice can make it seem as if you are not confident about what you are saying. " + self.passivity
		sentiment = ""
		overuse = " Repeating words can emphasize points, but also become distracting. " + self.overused_words
		text = start + ownership + passivity + sentiment + overuse
		return text