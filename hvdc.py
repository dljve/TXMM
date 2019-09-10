# -*- coding: utf-8 -*-
from __future__ import division
from itertools import permutations
from difflib import SequenceMatcher

def decode(codes):
    result = []
    number = {'1':'individual','2':'group',
              '3':'individual dead','3':'group dead',
              '5':'individual imaginary','6':'group imaginary',
              '7':'original form','8':'changed form'}
    sex = {'M':'male','F':'female','J':'joint','I':'indefinite'}
    id = {'F':'father','M':'mother','X':'parents','B':'brother',
          'T':'sister','H':'husband','W':'wife','A':'son',
          'D':'daughter','C':'child','I':'infant','Y':'family members',
          'R':'relative','K':'known','P':'prominent','O':'occupational',
          'E':'ethnic','S':'stranger','U':'uncertain'}
    age = {'A':'adult','T':'teenager','C':'child','B':'baby'}
    
    if type(codes) is str:
        codes = [codes]

    for code in codes:
        if code[1] == 'A':
            result.append((number[code[0]],'animal'))
        else:
            result.append((number[code[0]],sex[code[1]],id[code[2]],age[code[3]]))
            
    return result

# TODO if pred_chars < characters 
def match(pred_chars, true_chars):
    # Match ratio for evalution
    best_poss = None
    best_ratio = []
    n = len(true_chars)
    m  = len(pred_chars)
    if n == 0 or m == 0:
        return [0, 0, 0, 0, 0, 0, 0, 0]

    if n > m:
        chars1 = true_chars
        chars2 = pred_chars
    else:
        chars1 = pred_chars
        chars2 = true_chars
        
    # speed up calcualation
    perms = len(list(permutations(chars1, n)))
    if perms > 100000:
        return False
    
    for poss in list(permutations(chars1, n)):
        ratio = [0] * n
        for i in range(len(chars2)):
            ratio[i] = SequenceMatcher(None, poss[i], chars2[i]).ratio()
        mean_ratio = sum(ratio)/n
        mean_best_ratio = sum(best_ratio)/n
        if mean_ratio > mean_best_ratio:
            best_ratio = ratio
            best_poss = poss
    
    # Get category ratios
    al, numbers, sexes, ids, ages = 0, 0, 0, 0, 0
    for (best, true) in zip(best_poss, chars2):
        numbers += best[0] == true[0]
        sexes += best[1] == true[1]
        ids += best[2] == true[2]
        ages += best[3] == true[3]
        al += best == true
    
    number_ratio = numbers/n
    sex_ratio = sexes/n
    id_ratio = ids/n
    age_ratio = ages/n
    
    # For failure analysos
    return [best_poss, best_ratio, sum(best_ratio)/n, number_ratio, sex_ratio, id_ratio, age_ratio]
    
    # For summary statistics
    #return [al, numbers, sexes, ids, ages, min(n,m), m, n]
    