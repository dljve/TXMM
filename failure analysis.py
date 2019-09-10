# -*- coding: utf-8 -*-

import pandas as pd
from ast import literal_eval
import nltk
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.corpus import wordnet as wn
from nltk.parse import RecursiveDescentParser
import spacy
from fuzzywuzzy import fuzz
from pattern.en import pluralize, singularize
import hvdc

"""
Loading dataset and dream report sample
"""
df_male = pd.read_csv('hvdc_norms_male.csv') # Age is ADULT
df_female = pd.read_csv('hvdc_norms_female.csv')
df = pd.concat([df_male, df_female])
                
# ============================================================================
# NLTK, PyStatParser, Pattern, spaCy (can run from GPU)
# ============================================================================

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

"""
Determine whether a token is in a certain synset
Return a plural flag if the token is the plural of the synset
"""
def in_synset(token, name, check_plural=False):
    for synset in wn.synsets(token):
        syn_name = synset.name().split('.')[0]
        plural = (syn_name != token) and (syn_name == singularize(token))
        if syn_name == token or plural:
            hypernyms = synset.hypernym_paths()[0]
            if wn.synset(name) in hypernyms:
                if check_plural:
                    return [True, plural]
                else:
                    return True
        else:
            continue
    if check_plural:
        return [False, False]
    else:
        return False

# voice and face also refer that a person is there
def is_person(word):
    return in_synset(word,'person.n.01', check_plural=True)

def is_animal(word):
    return in_synset(word,'animal.n.01', check_plural=True)

# this function also catches lot of garbage
# nouns like 'room', 'house', 'street'
def is_social_group(word):
    return in_synset(word,'people.n.01') #in_synset(word,'social_group.n.01')

def is_known(word):
    return in_synset(word,'neighbor.n.01') or in_synset(word,'peer.n.01') \
        or in_synset(word,'acquaintance.n.01') or in_synset(word,'peer.n.01') \
        or in_synset(word,'relative.n.01') or in_synset(word,'kin.n.01') \
        or in_synset(word,'leader.n.01') or in_synset(word,'friend.n.01')

def is_professional(word):
    return in_synset(word,'professional.n.01') or in_synset(word,'employee.n.01') \
        or in_synset(word,'expert.n.01') or in_synset(word,'organization.n.01') \
        or in_synset(word,'skilled_worker.n.01')

def is_teenager(word):
    return in_synset(word,'adolescent.n.01')

def is_child(word):
    return in_synset(word,'child.n.01')

def is_baby(word):
    return in_synset(word,'baby.n.01')

# Remove duplicates based on token sort
# Could also remove based on similarity measures
# Synonyms are also possible but are very slow in wordnet 
# https://stackoverflow.com/questions/15730473/wordnet-find-synonyms
def is_duplicate(candidate, candidates):
    for c in candidates:
        if fuzz.token_sort_ratio(c,candidate) > 70:
            print 'Removed "'+c+'" == "'+candidate+'"'
            return True
    return False

# Wordnet or word embeddings    
def context_similarity(i, tokens):
    return None

def is_thirdpersonpronoun(noun):
    noun = noun.lower()
    if noun in ["he","him","his"]:
        return 'M'
    elif noun in ["she","her","hers"]:
        return 'F'
    else:
        return False


# Rule based character
# age of brother, sister, husband, son and daughter depend on the age of the dreamer
# Not included: Y = family member
# Not included: ex-husband, ex-wife, half-brother/sister
# You could use a text file for this for easier updating
lookup = { # Family
          '1MFA':['father','dad','pa','papa'],
          '1FMA':['mother','mom','ma','mama'],
          '2JXA':['parents'],
          '1MBA':['brother','bro'], '1FTA':['sister','s'],
          '1MHA':['husband'], '1FWA':['wife'],
          '1MAT':['son'], '1FDT':['daughter'],
          '1ICC':['child'], '1IIB':['infant'],
          # Relatives
          '1MRA':['grandpa','granddad','grandfather','stepfather','uncle','nephew'],
          '1FRA':['grandma','grandmom','grandmother','stepmother','aunt','niece'] 
          }

#wn.synsets('friend')[0].hypernym_paths()[0]

"""
Write loop to iterate over every dream and store in matrix
To calculate results
"""

nlp = spacy.load('en_core_web_sm')

# Get dream report from dataframe
sample = df.iloc[]
report = sample.Report
characters = sample.Characters
characters = literal_eval(characters)
# Check for no charactesr
if len(characters) == 1 and characters[0] == '':
    characters = []

# Apply spacy's natural language processing
doc = nlp(unicode(report))

pred_chars = []
roots = []
for sent in doc.sents:
    for chunk in sent.noun_chunks:     
        text, root_text, root_dep, head_text = chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text
        
        # Ignore duplicate noun roots (instead of fuzzy wuzzy)
        if root_text in roots:
            continue
        
        # to identify where a specific noun is:
        # chunk.start_char, chunk.end_char
        
        # If a third person pronoun is encountered
        # assume it refers to the last found entity and change the gender
        if is_thirdpersonpronoun(root_text) and pred_chars:
            number, sex, identity, age = list(pred_chars[-1])
            sex = is_thirdpersonpronoun(root_text)
            pred_chars[-1] = number+sex+identity+age
        
        # Initially we assume the age of the dreamer
        number, sex, identity, age = '1', 'I', 'U', 'A'
        is_character = False
    
        # Animals are classified as individuals or groups, but they are not classified by Sex, Identity, or Age.
        # (Coding symbol: 1ANI for a single animal; 2ANI for a group of animals.
        animal, plural = is_animal(root_text)
        if animal:
            is_character = True
            sex, identity, age = 'A', 'N', 'I'
            if plural:
                number = '2'
                
        # Find person
        person, plural = is_person(root_text)
        if person:
            is_character = True
            if plural:
                number, sex = '2', 'J'
            if is_professional(root_text):
                identity = 'O' # Occupational
        
        # Gender test
        if root_text.endswith("woman") or root_text.endswith("women") or root_text.endswith("girl") or root_text.endswith("girls") or root_text.endswith("maid") or root_text.endswith("maids"):
            sex = 'F'
        elif root_text.endswith("man") or root_text.endswith("men") or root_text.endswith("boy") or root_text.endswith("boys"):
            sex = 'M'
        
        # Find social group     
        if is_social_group(root_text):
            is_character = True
            number, sex = '2', 'J'
        
        # Is the entity known to the dreamer?
        if is_known(root_text):
            identity = 'K'
            
        # Age test
        if is_teenager(root_text):
            age = 'T'
        if is_child(root_text):
            age = 'C'
        if is_baby(root_text):
            age = 'B'                
        
        # NER dictionary lookup (family and relatives)
        found = False
        for code in lookup:
            if root_text in lookup[code]:
                found = True
                number,sex,identity,age = code[0],code[1],code[2],code[3]
                is_character = True
                break
        
        if is_character:
            print root_text + ' (' + text + ') ' + number+sex+identity+age
            pred_chars.append(number+sex+identity+age)
            roots.append(root_text)
    
# We will presume that prominent perons are Male and Adult
# Also check for fictional people here
for ent in doc.ents:
    if ent.label_ == 'PERSON' and is_person(ent.text.lower())[0]:
        pred_chars.append('1MPA')
        break

print hvdc.match(pred_chars, characters)
print characters