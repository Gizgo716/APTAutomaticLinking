import pandas
from pathlib import Path
import math
import itertools

filepath = Path('chains.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)

df = pandas.read_csv('Alternatives.csv')
column = 0

dataset = {}
outset = pandas.DataFrame()

print ("Reading Alternatives Matrix...")
while True:
    tech = f'T{column}'
    tech_conf = f"T{column} confidence"
    foundset = []
    if (tech not in df.columns):
        break
    outset.insert(loc = column, column=tech, value=None)

    for index, row in df.iterrows():
        if (not isinstance(row[tech], str)):
            break
        #print(f"Row {index}: {row[tech]}, {row[tech_conf]}")
        foundset.append((row[tech],row[tech_conf]))

    dataset[column] = foundset
    print(len(foundset))

    column += 1
outset.insert(loc = column, column="Confidence", value=None)

print(outset)

print ("Done")

combinations =  list(itertools.product(*dataset.values()))

print(len(combinations))
print(combinations)

for combination in combinations:
    print(combination)
    totalConfidence = 0
    new_row = []
    for tech in combination:
        new_row.append(tech[0])
        totalConfidence += tech[1]
    new_row.append(totalConfidence/column)
    new_df = pandas.DataFrame([new_row], columns=outset.columns)
    outset = pandas.concat([outset, new_df], ignore_index=True)

outset = outset.sort_values(by="Confidence", ascending=False)

outset.to_csv(filepath, index=False)
outset.to_html("Chains.html", index=False)

print(outset.head(10))