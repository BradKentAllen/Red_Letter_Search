# Red Letter Bible
''' Search Bible by topic
Preference to things Jesus said
Categorize remainder by OT, Paul letters, disciple letters
'''

# Rev 0.0.1 - Dev

import pandas as pd
from language_utils import Nat_Lang_Proc
from language_utils import Text_Utilities


class Red_Letter_Bible():
	def __init__(self, spaCy_core='small'):
		self.NLP = Nat_Lang_Proc()
		self.text_util = Text_Utilities()

		# get red letter DF
		redline_file = './Bible_texts/RedLetter_text.csv'
		redline_grouped_file = './Bible_texts/RL_grouped_text.csv'
		self.RedLetterDF = self.get_RedLetters(redline_file)
		self.RedLetterDF_grouped = self.get_RedLetters_grouped(redline_grouped_file)

	def reference_parser(self, reference):
		'''returns chapter and verse from reference
		of form -   chapter:verse
		'''
		reference = reference.split(':')
		return int(reference[0]), int(reference[1])

	def get_RedLetters(self, redline_file):
		'''create DF of Red Letter verses with reference
		Made for specific file
		'''
		redlineDF = pd.read_csv(redline_file, header=None, error_bad_lines=False)

		# drop column 3 as is non-used from header

		### this required when using the Red_Letter_text file
		redlineDF = redlineDF.iloc[:, :-1]

		redlineDF.columns = ['book', 'reference', 'verse']

		pd.set_option('display.expand_frame_repr', False)
		
		return redlineDF

	def get_RedLetters_grouped(self, redline_file):
		'''create DF of Red Letter verses with reference
		Specifically for grouped file
		'''
		redline_groupDF = pd.DataFrame(columns=['book', 'reference', 'verse'])
		with open(redline_file, 'r') as file:
			lines = file.readlines()

		for line in lines:
			line_list = line.split(',')
			separator = ','
			passage = separator.join(line_list[2:])
			#print(line_list[0], ':', line_list[1], '   ', passage)
			redline_groupDF = redline_groupDF.append({'book' : line_list[0] , 'reference' : line_list[1], 'verse': passage} , ignore_index=True)

		return redline_groupDF


	def word_search(self, word, word2=None, search='and', result=''):
		print('\nSTART RESULTS:')
		if result == 'grouped':
			searchDF = self.RedLetterDF_grouped
		else:
			searchDF = self.RedLetterDF

		verse_count = 0
		if word2 == None:
			for index, row in searchDF.iterrows():
				word_return = self.text_util.find_word(row[2], word)
				if word_return is not None:
					print(f'{row[2]} ({row[0]} {row[1]})')
					print('\n')
					verse_count +=1
			print(f'found {verse_count} verses with {word}')
		else:
			if search == '':
				for index, row in searchDF.iterrows():
					word_return = self.text_util.find_word(row[2], word)
					if word_return is not None:
						word2_return = self.text_util.find_word(row[2], word2)
						if word2_return is not None:
							print(f'{row[2]} ({row[0]} {row[1]})')
							print('\n')
							verse_count +=1
				print('\nSummary of Red Letter verses:')
				print(f"Found {verse_count} passage with '{word}' and '{word2}'")
			elif search == 'one':
				pass
			else:
				pass			
				

if __name__ == '__main__':
	print('start Red Letter app')
	RLapp = Red_Letter_Bible('small')
	#print('\nRed Letter verses: ')
	#print(RLapp.RedLetterDF.head())
	#print('\nRed Letter passages: ')
	#print(RLapp.RedLetterDF_grouped.head(20))

	#RLapp.spaCy_practice()

	# XXX Improvements
	# igore difference in caps (Scriptures)
	# get plural of word (Scripture and Scriptures)

	while True:
		result_type = input('grouped for passage or return for single verse: ')
		word = input("input first word (or exit): ")
		if word == 'exit' or word =='Exit':
			break
		word2 = input("..and second word: ")

		if word2 != '':
			search = input("one for either or return for both: ")
		else:
			word2 = None
			search = 'and'

		#### simple word search
		RLapp.word_search(word, word2, search, result_type)

	print('complete')

