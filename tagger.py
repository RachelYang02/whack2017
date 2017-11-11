"""
WHACK 2017
Input: questions.txt
Tag questions with labels given in file.
Output: json of Question Objects
"""

import re

def split_question(question):
	""" Split and return labels for each question. """
	question_and_labels = re.split('(?<=[.!?]) +',question)
	tags = re.sub('[(){}<>]', '', question_and_labels[1])
	tags = tags.split(", ")
	tags = [tag for tag in tags if tag is not None] 
	if len(tags) == 3:
		return (question_and_labels[0], tags[0], tags[1], tags[2])

def main(questions_l):
	""" Save each question and labels in dictionary, 
		and save collection of dictionaries in list. """
	questions_final = []
	for i, question in enumerate(questions_l):
		questions_dict = {}
		split_question(question)
		if split_question(question):
	 		(question_text, tag_difficulty, tag_length, tag_category) = split_question(question)
	 		questions_dict["name"] = "Question %d" % (i+1)
	 		questions_dict["text"] = question_text
	 		questions_dict["difficulty"] = tag_difficulty
	 		questions_dict["length"] = tag_length
	 		questions_dict["category"] = tag_category
	  		questions_final.append(questions_dict)
	return questions_final


def tagger(question_file):
	""" Read from question file,
		parse text, and save list of
		individual questions. """
	q = []
	with open(question_file, 'r') as questions_all:
		for question in questions_all:
			que = question.strip()
			if que:
				question = re.sub('[/]', '', question)
				q.append(question.strip())
		q = [x for x in q if x is not None]
		return main(q)

# See Results
tagger = tagger('questions.txt')
if tagger:
	print tagger
