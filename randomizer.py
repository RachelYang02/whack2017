"""
WHACK 2017
Input: json of Question dictionaries
Output: 3 questions of varying difficulty, length, and category
"""
import random
import json
from tagger import Tagger

class Randomizer():
	""" Randomize combination of difficulty, length, and category
		and select 3 questions to ask in interview. """

	def genRand(self,a,b):
		""" Generate random int i from range a <= i <= b. """
		return random.sample(xrange(a,b), 1)[0]

	def randomize(self):
		""" Generate random combination of difficulty, length, and category. """
		difficulty = self.genRand(0,2)
		length = self.genRand(0,2)
		category = self.genRand(0,3)
		return [difficulty, length, category]

	def get_q(self, questions_d, comb):
		""" Fetch question text given random combination. """
		for que in questions_d["questions"]:
			if comb == questions_d["questions"][que]["labels"]:
				return questions_d["questions"][que]["text"]			

	def main(self):
		""" Check to see if combination doesn't match label in question dict or
			if combination has been used before. 
			If so, try another random combination.
			If not, save question text to list.
			Output list of three questions. """
		three_q = []
		labels = ["first", "second", "third"]
		t = Tagger('questions.txt').tagger()
		q_dict = json.loads(t)

		while (len(three_q) < 4):
			comb = self.randomize()
			if self.get_q(q_dict, comb):
				if self.get_q(q_dict, comb) not in three_q:
					three_q.append(self.get_q(q_dict, comb))
				else:
					self.get_q(q_dict, self.randomize())
			else:
				self.get_q(q_dict, self.randomize())
		return three_q
