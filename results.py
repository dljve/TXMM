# -*- coding: utf-8 -*-
from __future__ import division

# get scores var from NER

import numpy as np
matrix = np.asarray(scores)

dreams_without_coding = sum(matrix[:,6:8].sum(1) == 0)
matrix = matrix[matrix[:,6:8].sum(1) > 0]

num_dreams = matrix.shape[0]
auto_codings = matrix[:,6].sum()
human_codings = matrix[:,7].sum()

# ppa
mins = np.minimum(matrix[:,6],matrix[:,7])
pres_ppa = np.true_divide(mins.sum(), np.maximum(matrix[:,6],matrix[:,7]).sum() )
number_ppa = np.true_divide( matrix[:,1].sum(), mins.sum())
gender_ppa = np.true_divide( matrix[:,2].sum(), mins.sum())  
id_ppa = np.true_divide( matrix[:,3].sum(), mins.sum())  
age_ppa = np.true_divide( matrix[:,4].sum(), mins.sum()) 
all_ppa = np.true_divide( matrix[:,0].sum(), mins.sum()) 


print "Category\tNumber of dreams\tAutomized codings\tHuman codings\tPercent perfect agreement"
print "_________________________________________________________________________________________________________"
print "Characters\t"+str(num_dreams)+"\t\t\t"+str(auto_codings)+"\t\t\t"+str(human_codings)
print "  Presence\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % pres_ppa
print "  Number\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % number_ppa
print "  Gender\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % gender_ppa
print "  Identity\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % id_ppa
print "  Age\t\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % age_ppa
print "  All correct\t"+str(num_dreams)+"\t\t\t\t\t\t\t\t%.4f" % all_ppa