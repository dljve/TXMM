# TXMM
Code for a rule-based system based on WordNet, accompanying the paper "Automatic character coding in dream reports" for Text and Multimedia Mining.

>**ABSTRACT**
>This paper explores the possibility of automating the character coding
>process of the Hall-Van de Castle system for dream annotation.
>We propose a rule-based system that utilizes WordNet, named entity
>recognition and coreference resolution. The reliability of this system
>is evaluated by the percentage-of-agreement method. Although
>the system’s reliability is not yet good enough for practical purposes,
>the results are still very promising and suggest that further
>development could lead to a reliable automatic coding system.

- _NER.py_: main file to perform named entity recognition (and automatic coding) on dream reports.
- _dreamcloud.py_: generates word clouds to get an idea of the main themes in (fe)male dreams. This is used for the exploratory data analysis (EDA) phase.
- _hvdc.py_: helper functions for the Hall-Van de Castle coding system
- _hvdc_norms_{male,female}.{htm,csv}: the norm dreams for male and female in csv (processed) and htm (unprocessed) format.
- _preprocess.py_: scrapes the dreams from the htm file and stores them in a csv file.
- _leave one out.txt_: results of leave-one-out analysis by running _results.py_
- _results.py_: calculates the percent perfect agreement (with the human coder) for the 5 character categories
