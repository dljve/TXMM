# -*- coding: utf-8 -*-

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

male = pd.read_csv('hvdc_norms_male.csv').Report.sum()
female = pd.read_csv('hvdc_norms_female.csv').Report.sum()

wordcloudm = WordCloud(width=800, height=400).generate(male)
wordcloudf = WordCloud(width=800, height=400).generate(female)

plt.figure( figsize=(20,10) )
plt.imshow(wordcloudm, interpolation='bilinear')
plt.axis("off")
plt.show()

plt.figure( figsize=(20,10) )
plt.imshow(wordcloudf, interpolation='bilinear')
plt.axis("off")
plt.show()