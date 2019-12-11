#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:57:59 2019

@author: shardsofblue
"""

# Import packages
import re # For regex
import itertools # For collapsing nested lists
import functools # For reducing tuples
import operator # For adding tuples
from nltk.tokenize import sent_tokenize # For tokenizing sentences
import pandas as pd

# Set correct file path
# Run -> Configuration per file -> 'The directory of the file being executed'
import os
THIS_FOLDER = os.path.dirname(os.path.abspath('__file__'))

#####################################
#### DATA LOAD AND PREPROCESSING ####
#####################################

### Load in test data

# Returns a list (all articles) of lists (each article) of strings (each line)
# One article: test_articles[0]
# One line in the article: test_articles[0][0]
test_articles = [open(os.path.join(THIS_FOLDER, 'sample-articles/infowars-1.txt'),"r+").readlines(), #0
                 open(os.path.join(THIS_FOLDER, 'sample-articles/infowars-2.txt'),"r+").readlines(), #1
                 open(os.path.join(THIS_FOLDER, 'sample-articles/nyt-1.txt'),"r+").readlines(), #2
                 open(os.path.join(THIS_FOLDER, 'sample-articles/nyt-2.txt'),"r+").readlines(), #3
                 open(os.path.join(THIS_FOLDER, 'sample-articles/breitbart-1.txt'),"r+").readlines(), #4
                 open(os.path.join(THIS_FOLDER, 'sample-articles/breitbart-2.txt'),"r+").readlines(), #5
                 open(os.path.join(THIS_FOLDER, 'sample-articles/foxnews-1.txt'),"r+").readlines(), #6
                 open(os.path.join(THIS_FOLDER, 'sample-articles/foxnews-2.txt'),"r+").readlines(), #7
                 open(os.path.join(THIS_FOLDER, 'sample-articles/huffpost-1.txt'),"r+").readlines(), #8
                 open(os.path.join(THIS_FOLDER, 'sample-articles/huffpost-2.txt'),"r+").readlines(), #9
                 open(os.path.join(THIS_FOLDER, 'sample-articles/usatoday-1.txt'),"r+").readlines(), #10
                 open(os.path.join(THIS_FOLDER, 'sample-articles/usatoday-2.txt'),"r+").readlines() #11
                 ]

#### Clean up the data ####

# Function: Clean an article (a list of strings)
def clean_article(article):
    clean_lines = []
    # Clean each line (a string)
    for line in article:
        clean_lines.append(line.rstrip().lower())
    # Remove blank lines
    for line in clean_lines:
        if line == "":
            clean_lines.pop(clean_lines.index(line))
    return clean_lines
# Test the function
# clean_article(test_articles[0])

# Function: Clean all articles
def clean_all(list_of_articles):
    clean_articles = []
    for article in list_of_articles:
        clean_articles.append(clean_article(article))
    return clean_articles
# Test the function
# clean_all(test_articles)
    
# Apply clean_all()
test_articles_c = clean_all(test_articles)
#test_articles_c[0]

# Delete obsolete variable
del test_articles

# Function: Combine lines in an article (excludes title)
def combine_lines(article):
    all_content = ''
    for line in article:
        if article.index(line) != 0:
            all_content += line + ' '
    return all_content
# Test the function
# combine_lines(test_articles_c[1])


#### Take the clean articles and load them into a more complex data structure to store more info about them ####
    
# Function: Get a title
def get_title(list_):
    title = list_[0]
    return title
# Test the function
# get_title(test_articles_c[1])

# Function: Get all titles
def get_titles(list_of_lists):
    titles = []
    for i in range(len(list_of_lists)):
        titles.append(get_title(list_of_lists[i]))
    return titles
# Test the function
# get_titles(test_articles_c)

### Store the data
# Access all of a publication: article_dict['usatoday']
# Access all of an article: article_dict['usatoday'][1]
# Access title of an article: article_dict['usatoday'][1]['title']
article_dict = {
        'infowars' : [
                  {'title' : get_title(test_articles_c[0]),
                   'lines' : test_articles_c[0][1:], # start from 1 to skip title
                   'article_text': combine_lines(test_articles_c[0]),
                   'article_id': 'infowars1'
                   },
                  {'title' : get_title(test_articles_c[1]),
                   'lines' : test_articles_c[1][1:],
                   'article_text': combine_lines(test_articles_c[1]),
                   'article_id': 'infowars2'
                   }
                ],
        'nyt' : [
                  {'title' : get_title(test_articles_c[2]),
                   'lines' : test_articles_c[2][1:],
                   'article_text': combine_lines(test_articles_c[2]),
                   'article_id': 'nyt1'
                   },
                  {'title' : get_title(test_articles_c[3]),
                   'lines' : test_articles_c[3][1:],
                   'article_text': combine_lines(test_articles_c[3]),
                   'article_id': 'nyt2'
                   }
                ],
        'breitbart' : [
                  {'title' : get_title(test_articles_c[4]),
                   'lines' : test_articles_c[4][1:],
                   'article_text': combine_lines(test_articles_c[4]),
                   'article_id': 'breitbart1'
                   },
                  {'title' : get_title(test_articles_c[5]),
                   'lines' : test_articles_c[5][1:],
                   'article_text': combine_lines(test_articles_c[5]),
                   'article_id': 'breitbart2'
                   }
                ],
        'foxnews' : [
                  {'title' : get_title(test_articles_c[6]),
                   'lines' : test_articles_c[6][1:],
                   'article_text': combine_lines(test_articles_c[6]),
                   'article_id': 'foxnews1'
                   },
                  {'title' : get_title(test_articles_c[7]),
                   'lines' : test_articles_c[7][1:],
                   'article_text': combine_lines(test_articles_c[7]),
                   'article_id': 'foxnews2'
                   }
                ],
        'huffpost' : [
                  {'title' : get_title(test_articles_c[8]),
                   'lines' : test_articles_c[8][1:],
                   'article_text': combine_lines(test_articles_c[8]),
                   'article_id': 'huffpost1'
                   },
                  {'title' : get_title(test_articles_c[9]),
                   'lines' : test_articles_c[9][1:],
                   'article_text': combine_lines(test_articles_c[9]),
                   'article_id': 'huffpost2'
                   }
                ],
        'usatoday' : [
                  {'title' : get_title(test_articles_c[10]),
                   'lines' : test_articles_c[10][1:],
                   'article_text': combine_lines(test_articles_c[10]),
                   'article_id': 'usatoday1'
                   },
                  {'title' : get_title(test_articles_c[11]),
                   'lines' : test_articles_c[11][1:],
                   'article_text': combine_lines(test_articles_c[11]),
                   'article_id': 'infowars1'
                   }
                ]
        }
    

# Delete obsolete variable
del test_articles_c

# Function: Tokenize the words in a single article
def tokenize_words(article_string):
    tokenized = re.split("[, \-!?:\t\.]+", article_string)
    return tokenized
# Test the function
#tokenize_words(article_dict['infowars'][0]['article_text'])
    
### Add TOKENIZED WORDS,SENTENCES fields
# For each publication
for pub in article_dict: 
    # For each set of articles
    for article_data in article_dict[pub]:
        # For each (of two) articles (a list of (2) dictionaries)
        i=0 # Counter for a the list of dictionaries
        while i < len(article_dict[pub]): 
            # Add tokenized words
            article_dict[pub][i]['words'] = tokenize_words(article_dict[pub][i]['article_text']) 
            # Add word count
            article_dict[pub][i]['total_words'] = len(article_dict[pub][i]['words']) 
            # Add tokenized sentences
            article_dict[pub][i]['sentences'] = sent_tokenize(article_dict[pub][i]['article_text'])
            # Add sentence count
            article_dict[pub][i]['total_sentences'] = len(article_dict[pub][i]['sentences'])
            i+=1 
# Clear obsolete variables
del [article_data, i, pub]
#article_dict['usatoday'][1]['total_sentences']

####################
#### HEDGE WORK ####
####################

# Bag of Regex
hedging_patterns = ['(alleg)\w+', 
                 'perhaps',
                 'maybe',
                 '(sugges)\w+',
                 'similar',
                 'may',
                 'might',
                 'apparently',
                 'possibl',
                 'claim',
                 'likely',
                 'believe',
                 'think',
                 'seem',
                 #re.compile('suspect'), # need to parse for noun
                 'as far as I know',
                 '(if)\W+(?:\w+\W+){0,5}?(true)',
                 '(if)\W+(?:\w+\W+){1,2}?(was in fact)',
                 'i guess',
                 'reason to doubt',
                 'speculat',
                 'an alternative theory',
                 'suppose',
                 '(some)\W+(?:\w+\W+){1,2}?(say)',
                 'it is clear'
                 ]

# Function: Count number of hedge words per article
def find_hedges(string_):
    hedge_count = 0
    hedges = []
    # For each hedging pattern
    for i in hedging_patterns:
        try:
            # Search for all instances of the pattern
            found = re.findall(i, string_, re.DOTALL)
            if found:
                # Increment the hedge counter
                hedge_count += len(found)
                # If the thing found is a split phrase (it will read as a tuple),
                # combine it into a string as a list item
                if isinstance(found[0], tuple):
                    found = functools.reduce(operator.add, found)
                    found = [' ... '.join(found)]
                # Add the newly-found hedge to the list of words for that article
                hedges.append(found)
        except:
            pass
    # Collapse the list of lists into a list of strings
    hedges = list(itertools.chain.from_iterable(hedges))
    return [hedge_count, hedges]
# Test the function
# find_hedges(article_dict['infowars'][1]['article_text'])

# Function: Find hedge sentences
def find_hedge_sents(list_):
    sent_count = 0
    hedge_sent = []
    # For each sentence in the list
    for sent in list_:
        # For each hedging pattern
        for i in hedging_patterns:
            #print(sent)
            try: 
                found = re.search(i, sent)
                if found and (sent not in hedge_sent): # and not in hedge_sent already
                    sent_count += 1
                    hedge_sent.append(sent)
            except:
                pass
    return [sent_count, hedge_sent]
# Test the function
#find_hedge_sents(article_dict['infowars'][0]['sentences'])
#re.search('(alleg)\w+', article_dict['infowars'][0]['sentences'][0]).group()

### Add HEDGE WORDS and SENTENCES to data
# For each publication
for pub in article_dict: 
    # For each set of articles
    for article_data in article_dict[pub]:
        # For each (of two) articles (a list of (2) dictionaries)
        i=0 # Counter for a the list of dictionaries
        while i < len(article_dict[pub]): 
            # Add hedge words
            article_dict[pub][i]['hedge_words'] = find_hedges(article_dict[pub][i]['article_text'])[1]
            # Add hedge word count
            article_dict[pub][i]['total_hedge_words'] = find_hedges(article_dict[pub][i]['article_text'])[0]
            # Find percent of hedge words to words
            article_dict[pub][i]['hedge_perc_words'] = round(article_dict[pub][i]['total_hedge_words'] / article_dict[pub][i]['total_words']*100, 2)
            # Add hedge sentences
            article_dict[pub][i]['hedge_sentences'] = find_hedge_sents(article_dict[pub][i]['sentences'])[1]
            # Add hedge sentence count
            article_dict[pub][i]['total_hedge_sentences'] = find_hedge_sents(article_dict[pub][i]['sentences'])[0]
            # Find percent of sentences are hedging sentences
            article_dict[pub][i]['hedge_perc_sentences'] = round(article_dict[pub][i]['total_hedge_sentences'] / article_dict[pub][i]['total_sentences']*100, 2)
            # Add article identifier 
            article_dict[pub][i]['article_id'] = pub + str(i+1)
            i+=1 
# View just one entry
# article_dict['nyt'][1]['total_hedge_words']
        
# Delete obsolete variables
del [i, pub, article_data]

# Function: Find average hedge amount per pub
def avg_hedge_words(dict_):
    return round((dict_[0]['hedge_perc_words'] + dict_[1]['hedge_perc_words']) / 2, 2)
# Test the function
avg_hedge_words(article_dict['infowars'])

# Function: Find average hedge amount per pub
def avg_hedge_sents(dict_):
    return round((dict_[0]['hedge_perc_sentences'] + dict_[1]['hedge_perc_sentences']) / 2, 2)
# Test the function
avg_hedge_sents(article_dict['infowars'])

### Store HEDGE AVERAGES
pub_dict = {
        'infowars' :
            {'ideology' : 'RCON',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['infowars']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['infowars'])
             },
        'nyt' : 
            {'ideology' : 'L',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['nyt']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['nyt'])
             },
        'breitbart' : 
            {'ideology' : 'RR',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['breitbart']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['breitbart'])
             },
        'foxnews' : 
            {'ideology' : 'R',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['foxnews']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['foxnews'])
             },
        'huffpost' : 
            {'ideology' : 'LL',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['huffpost']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['huffpost'])
             },
        'usatoday' :
            {'ideology' : 'C',
             'avg_hedge_word_perc' : avg_hedge_words(article_dict['usatoday']),
             'avg_hedge_sent_perc' : avg_hedge_sents(article_dict['usatoday'])
             },
        }



#### View hedges info or each publication
for pub in article_dict:
    i=0
    # For each article
    while i < len(article_dict[pub]):
        print(pub, '\n', 
              'article id: ', article_dict[pub][i]['article_id'], '\n',
              'title:', article_dict[pub][i]['title'], '\n',
              'hedge words: ', article_dict[pub][i]['hedge_words'], '\n', 
              'count words: ', ' ', article_dict[pub][i]['total_words'], '\n',
              'count hedge words: ', article_dict[pub][i]['total_hedge_words'], '\n', 
              'percent of words are hedges: ', article_dict[pub][i]['hedge_perc_words'], '\n',
              'count sentences: ', article_dict[pub][i]['total_sentences'], '\n',
              'count hedge sentences: ', article_dict[pub][i]['total_hedge_sentences'], '\n',
              'percent of sentences are hedges: ', article_dict[pub][i]['hedge_perc_sentences'], '\n',
              sep='')
        i+=1
# =============================================================================
# View the data in the console 
# For each publication
# for pub in pub_dict:
#     print(pub, ':', sep='')
#     for data in pub_dict[pub]:
#         print(data, ': ', pub_dict[pub][data])
#     print('\n')
# =============================================================================


#### Convert the articles dictionary to a Pandas DataFrame ####
# Publication Name | Article Name | Total Words | Total Hedge Words | Perc Hedge Words
    
article_info_df = pd.DataFrame(columns=['title', 'total_words', 'total_hedge_words', 'hedge_perc_words', 'total_sentences', 'total_hedge_sentences', 'hedge_perc_sentences']) # init dataframe

# For each publication
for pub in article_dict:
    i=0
    # For each article
    while i < len(article_dict[pub]):
        article_info_df = article_info_df.append(pd.DataFrame([article_dict[pub][i]]).filter(items=['title', 'total_words', 'total_hedge_words', 'hedge_perc_words', 'total_sentences', 'total_hedge_sentences', 'hedge_perc_sentences']), ignore_index=True)
        i+=1

# Add publication titles (manually)
article_info_df['publication']=['infowars', 'infowars', 
                'nyt', 'nyt', 
                'breitbart', 'breitbart', 
                'foxnews', 'foxnews', 
                'huffpost', 'huffpost', 
                'usatoday', 'usatoday']

        

# Reorganize the cols
cols = article_info_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
article_info_df = article_info_df[cols]
# CONTINUED AFTER PUBLICATIONS DF

# Delete obsolete variables
del [i, pub, cols]

### Convert publications dictionary to Pandas DataFrame
# Add data items for each publication in the dictionary
pub_dict_df = pd.DataFrame() # init dataframe
for pub in pub_dict:
    pub_dict_df = pub_dict_df.append(pd.DataFrame([pub_dict[pub]]), ignore_index=True)
# Add publication title column
all_pubs = list(pub_dict.keys()) # init list of publications
for i in range(len(all_pubs)):
    pub_dict_df.loc[i, 'publication'] = all_pubs[i]
    
# Delete obsolete variable
del [i, pub, all_pubs]

# Set index to publication title
pub_dict_df = pub_dict_df.set_index('publication')
# Reverse column order
pub_dict_df = pub_dict_df.iloc[:, ::-1]

# Export it!
pub_dict_df.to_csv(os.path.join(THIS_FOLDER, 'csvs/publication-findings.csv'))

# Split out the sentences and words info into two different dataframes for viewing in Spyder
pub_df_words = pub_dict_df.drop(columns=['avg_hedge_sent_perc'])
pub_df_sent = pub_dict_df.drop(columns=['avg_hedge_word_perc'])

### BACK TO ARTICLE DF PROCESSING
# Join the publications info to the article info
article_info_df = article_info_df.join(pub_dict_df, on='publication').drop(columns=['avg_hedge_sent_perc', 'avg_hedge_word_perc'])

# Reorganize the cols (again)
cols = article_info_df.columns.tolist()
cols = cols[0:1] + cols[-1:] + cols[1:-1]
article_info_df = article_info_df[cols]

# Export it!
article_info_df.to_csv(os.path.join(THIS_FOLDER, 'csvs/article-findings.csv'))

# Split out the sentences and words info into two different dataframes for viewing in Spyder
article_words_df = article_info_df.drop(columns=['total_sentences', 'total_hedge_sentences', 'hedge_perc_sentences'])
article_sents_df = article_info_df.drop(columns=['total_words', 'total_hedge_words', 'hedge_perc_words'])

# Delete obsolete variable
del cols

#### Put hedge words and sentences into dataframes ####
# Publication | Word 
words_found_df = pd.DataFrame(columns=['publication', 'article', 'hedge_word']) # init dataframe
# For each publication
row = 0
for pub in article_dict:
    i=0
    # For each article
    while i < len(article_dict[pub]):
        for word in article_dict[pub][i]['hedge_words']:
            words_found_df.loc[row] = [pub] + [pub + str(i+1)] + [word]
            row+=1
        i+=1
# Export it!
words_found_df.to_csv(os.path.join(THIS_FOLDER, 'csvs/hedge-words-found.csv'))

sentences_found_df = pd.DataFrame(columns=['publication', 'article', 'hedged_sentence']) # init dataframe
# For each publication
row = 0
for pub in article_dict:
    i=0
    # For each article
    while i < len(article_dict[pub]):
        for word in article_dict[pub][i]['hedge_sentences']:
            sentences_found_df.loc[row] = [pub] + [pub + str(i+1)] + [word]
            row+=1
        i+=1
# Export it!
sentences_found_df.to_csv(os.path.join(THIS_FOLDER, 'csvs/hedge-sentences-found.csv'))

# Delete obsolete variable
del [i, pub, row, word]
        
### TO DOs
# find counts of unique hedge words(?) <- this seems like a "gee wiz" only
# What about some nice bar graphs? Common hedge words?
# give each article a name in the DFs (nyt2, infowars1, etc.)
# average hedge words per sentence? per hedging sentence?