import pandas
from pathlib import Path
import math
import itertools
import configparser

class ChainGen:

    def prepare(self):
        config = configparser.ConfigParser()
        config.read("..\config.cfg")

        filepath = Path(config.get("paths","outputpath") + 'Chains.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df = pandas.read_csv(config.get("paths","outputpath") +'Alternatives.csv')
        column = 0
        possible = 1

        dataset = {}
        self.outset = pandas.DataFrame()

        print ("Reading Alternatives Matrix...")
        while True:
            tech = f'T{column}'
            tech_conf = f"T{column} confidence"
            foundset = []
            if (tech not in df.columns):
                break
            self.outset.insert(loc = column, column=tech, value=None)

            for index, row in df.iterrows():
                if (not isinstance(row[tech], str)):
                    break
                #print(f"Row {index}: {row[tech]}, {row[tech_conf]}")
                foundset.append((row[tech],row[tech_conf]))

            dataset[column] = foundset
            possible *= len(foundset)

            column += 1
        self.outset.insert(loc = column, column="Confidence", value=None)

        self.dataset = dataset
        self.column = column
        self.filepath = filepath
        self.config = config

        print ("Done")
        return possible

    def combine(self):

        combinations =  list(itertools.product(*self.dataset.values()))

        #print(len(combinations))
        #print(combinations)

        for combination in combinations:
            #print(combination)
            totalConfidence = 0
            new_row = []
            for tech in combination:
                new_row.append(tech[0])
                totalConfidence += tech[1]
            new_row.append(totalConfidence/self.column)
            new_df = pandas.DataFrame([new_row], columns=self.outset.columns)
            self.outset = pandas.concat([self.outset, new_df], ignore_index=True)

        self.outset = self.outset.sort_values(by="Confidence", ascending=False)

        self.outset.to_csv(self.filepath, index=False)
        self.outset.to_html(self.config.get("paths","outputpath") + "Chains.html", index=False)

        print(f"Showing top {int(self.config.get('other', 'chainPreview', fallback=0))} results")
        print(self.outset.head(int(self.config.get("other", "chainPreview"))))