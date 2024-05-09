#!/usr/bin/env python

# Zipfian
# 
# A simple word processing program
# to extract statistical information
# from natural language in relation
# to computational linguistical models.

import re
import argparse
import numpy as np
import matplotlib.pyplot as plt


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
filename = args.filename

try:
	file = open(filename, "r")
except Exception as e:
	print("Unable to open file ", filename)
	exit(1)


# Filter a line of text to remove punctuation
def filter_text(text):
	s = ""
	for c in text:
		s += c.lower() if c.isalnum() else " "
	return s


# Read and filter the text
text = ""
text_filtered = ""
for line in file.readlines():
	text += line
	text_filtered += filter_text(line)

text_filtered = re.sub(r'\s+', ' ', text_filtered)


# Get a list of all the words
words_list = text_filtered.split()

# Dictionary of words and their number of appearances
words = dict({})

# Total number of words
words_total_number = len(words_list)


# Construct a dictionary of the words
# in the text and their frequency
for word in words_list:

	if word in words:
		words[word] += 1
	else:
		words.update({word: 1})


# Process the dictionary to
# extract statistical information

# Words sorted by word count
words_sorted = list(sorted(words.items(), key = lambda item : -item[1]))


# List of words sorted by frequency
words_frequency = [
	(word, count / words_total_number)
	for word, count in words_sorted
]

# Number of words with only one appearance
words_rare = 0
for word in words:
	if words[word] == 1:
		words_rare += 1

print("-" * 5, "Word Analysis", "-" * 5)
print("  Unique words =", words_total_number)
print("  Rare words =", words_rare)
print("  Most frequent word = \"" + words_frequency[0][0] +
	"\" (freq. =", round(words_frequency[0][1], 2) ,")")
print("-" * 25)


x = np.log(np.arange(1, len(words_frequency) + 1))
y = np.log([ item[1] for item in words_frequency ])
plt.xlabel("Word Rank")
plt.ylabel("Word Frequency")
plt.scatter(x, y, alpha = 1)
plt.show()
