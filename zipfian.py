#!/usr/bin/env python

# Zipfian
# 
# A simple word processing program
# to extract statistical information
# from natural language in relation
# to computational linguistical models
# and machine learning.

import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
# import scipy.sparse


# Filter a line of text to remove punctuation
def remove_punctuation(text) -> str:
	s = ""
	for c in text:
		s += c.lower() if c.isalnum() else " "
	return s


# A simple structure to hold processed text results
class ProcessedText(object):

	# tokens -> Text subdivided as a list of words
	# words -> Dictionary of words and their count
	# words_sorted -> List of words sorted by descending frequency
	# words_frequency -> Sorted list of words and their frequency
	# rare_words -> Number of words with only one appearance
	# unique_words -> Number of unique different words in the text

	def __init__(self, text):
		
		# Filter and tokenize text
		self.tokens = re.sub(
			r'\s+', ' ', remove_punctuation(text)
		).split()

		# Dictionary of words and their count of appearances
		self.words = dict({})
		for word in self.tokens:

			if word in self.words:
				self.words[word] += 1
			else:
				self.words.update({word: 1})

		# Words sorted by word count
		self.words_sorted = list(
			sorted(self.words.items(), key = lambda item : -item[1])
		)

		# List of words sorted by frequency
		self.words_frequency = [
			(word, count / len(self.tokens))
			for word, count in self.words_sorted
		]

		# Count words with only one appearance
		self.rare_words = 0
		for word in self.words:
			if self.words[word] == 1:
				self.rare_words += 1

		# Count the number of different words
		self.unique_words = len(self.words_frequency)


# Entry point for execution when called as a script.
def main():

	# Get the filename as a command-line argument
	# and try to open the file
	parser = argparse.ArgumentParser(
		description = "A simple word processing program \
		to extract statistical information from natural \
		language in relation to computational linguistical models."
	)

	parser.add_argument(
		"filename",
		help = "The file containing the natural language to process"
	)

	args = parser.parse_args()

	try:
		file = open(args.filename, "r")
	except Exception as e:
		print("Unable to open file ", args.filename)
		exit(1)

	text = file.read()

	# Process the raw text
	proc_text = ProcessedText(text);

	print("-" * 5, "Word Analysis", "-" * 5)
	print("  Unique words =", proc_text.unique_words)
	print("  Rare words =", proc_text.rare_words)
	print("  Most frequent words: ")
	for i in range(5):
		print(
			"   ", proc_text.words_frequency[i][0],
			"(freq. = ", round(proc_text.words_frequency[i][1] * 100, 1), "%)"
		)
	print()


	# Plot the word frequency against word rank
	# in log-log scale to verify Zipf's law
	plt.title("Zipf's Law")
	plt.xlabel("Word Rank")
	plt.ylabel("Word Frequency")

	log_ranks = np.log(np.arange(1, len(proc_text.words_frequency) + 1))
	log_frequency = np.log([ item[1] for item in proc_text.words_frequency ])

	# Fit log-log data to a line
	# The 10% most frequent and 40% least frequent words are cut out
	# to fit the bulk
	zipf_a, zipf_b = np.polyfit(
		log_ranks[
			int(0.1 * proc_text.unique_words) : int(0.6 * proc_text.unique_words)],
		log_frequency[
			int(0.1 * proc_text.unique_words) : int(0.6 * proc_text.unique_words)],
		1
	)

	plt.plot(log_ranks, log_ranks * zipf_a + zipf_b)

	print(f"  Linear Model: {round(zipf_a, 3)} * x + {round(zipf_b, 3)}")

	plt.scatter(
		log_ranks,
		log_frequency,
		alpha = 1
	)


	print("-" * 5, "Markov Analysis", "-" * 5)
	print("Starting Markov chain construction...")


	# markov_matrix = csr_matrix(
	# 	shape = (proc_text.unique_words, proc_text.unique_words),
	# 	dtype = float
	# )

	# for i in range(1, len(proc_text.tokens)):
	# 	markov_matrix ...


	print(" ", len(proc_text.tokens), "words analyzed")
	print("Finished constructing the Markov chain matrix.")


	plt.show()


if __name__ == '__main__':
	main()
