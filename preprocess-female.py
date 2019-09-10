# -*- coding: utf-8 -*-
"""
HVDC scraper
"""
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

soup = BeautifulSoup( open("hvdc_norms_female.htm"), "html.parser" )

reports = re.findall(u'#\d\d\d\d (.+?)\s*?\([0-9]+\s*?words\)', soup.getText(), re.DOTALL)
characters = re.findall(u'Number: \d\d\d\d.*?OBJ.(?:\n{5})?(.*?)\n\n\n\n(?:\n|\t)', soup.getText(), re.DOTALL)

# exclude newlines from reports
reports = [report.replace('\n','') for report in reports]

# remove characters with a missing report
missing = [146] # hvdc female dreams without report
for i in sorted(missing, reverse=True):
    del characters[i-1]

# keep a list of lists of characters
characters = [character.split('\n') for character in characters]  

# save to a dataframe
df = pd.DataFrame(zip(reports,characters),columns=['Report','Characters'])
df.to_csv('hvdc_norms_female.csv',',',index=False)