import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import os.path



import csv
values = []
with open('CitronResearch.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
        values.append((row[5], row[7] ))
print(values)

train = values[:289]
test = values[289:]

dictionary = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
dictionary

t = [({word: (word in word_tokenize(x[0])) for word in dictionary}, x[1]) for x in train]


classifier = nltk.NaiveBayesClassifier.train(t)
test_data = test[1][0]
test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in dictionary}
print (classifier.classify(test_data_features))

with open('CitronResearch2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    with open('CitronResearch3.csv', 'w') as csvfile_w:
        csv_writer = csv.writer(csvfile_w, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            i = i + 1
            if i < 289:
                csv_writer.writerow(row)
                continue
            test_data = test[i-289][0]
            test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in dictionary}
            row[7] = classifier.classify(test_data_features)
            csv_writer.writerow(row)
  

