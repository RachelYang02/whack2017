"""
WHACK 2017
Input: questions.txt
Tag questions with labels given in file.
Output: json of Question Dictionaries
"""

import re
import json

class Tagger():
	""" Parse input text file of questions and create 
		json of Question Dictionaries (question_text, labels)."""
	def __init__(self, question_file):
		self.question_file = question_file

	def split_question(self, question):
		labels_difficulty = ["easy", "medium", "hard"]
		labels_length = ["short", "medium", "long"]
		labels_category = ["Interpersonal Skills", "Leadership", "Failure_Frustration", "Time Management_Prioritization"]
		""" Split and return labels for each question. """
		question_and_labels = re.split('(?<=[.!?]) +',question)
		tags = re.sub('[(){}<>]', '', question_and_labels[1])
		tags = tags.split(", ")
		tags = [tag for tag in tags if tag is not None] 
		if len(tags) == 3:
			tags[0] = labels_difficulty.index(tags[0])
			tags[1] = labels_length.index(tags[1])
			tags[2] = labels_category.index(tags[2])
			return (question_and_labels[0], tags)

	def json_build(self, questions_l):
		""" Save each question and labels in dictionary, 
			and save collection of dictionaries in list. """
		questions_final = {}
		questions_dict = {}
		for i, question in enumerate(questions_l):
			questions_tags_dict = {}
			self.split_question(question)
			if self.split_question(question):
		 		(question_text, tags) = self.split_question(question)
		 		questions_tags_dict["text"] = question_text
		 		questions_tags_dict["labels"] = tags

		 		questions_dict["Question %d" % (i+1)] = questions_tags_dict
		questions_final["questions"] = questions_dict
		questions_json = json.dumps(questions_final)
		return questions_json


	def tagger(self):
		""" Read from question file,
			parse text, and save list of
			individual questions. """
		q = []
		with open(self.question_file, 'r') as questions_all:
			for question in questions_all:
				que = question.strip()
				if que:
					question = re.sub('[/]', '', question)
					q.append(question.strip())
			q = [x for x in q if x is not None]
			return self.json_build(q)