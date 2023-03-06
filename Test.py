import pandas
import numpy as np
df = pandas.read_csv('Spreadsheet.csv')
attack = pandas.read_csv('Attack.csv')
sep = '.'
#print(df["Technique"][0])

#print(df.shape)

#print(attack["TestId"][0])

print(df["TestId"][0])
print(df["TestId"][0].split(sep, 1)[0])
def Output(id, confidence):
    return

for i in range(attack.shape[0]):
    for j in range(df.shape[0]):

        partial = df["TestId"][j].split(sep, 1)[0]
        inputlist = df["Input Type"][j].split('/')
        outputlist = df["Output Type"][j].split('/')

        #look for exact match ID
        if(df["TestId"][j] == attack["TestId"][i]):
            print("matched exact")
            Output(j, 1.0)

        #look for partial match ID
        if(partial == attack["TestId"][i]):
            #calculate confidence
            print("match")

        