import pandas
from pathlib import Path
import configparser

class AltGen:

    def run():

        config = configparser.ConfigParser()
        config.read("..\config.cfg")

        BYPASS_OS = config.getboolean("other","dropOS")
        TID_WEIGHT = float(config.get("weights","testID"))
        TACTIC_WEIGHT = float(config.get("weights","tactic"))
        TECHNIQUE_WEIGHT = float(config.get("weights", "technique"))
        INPUT_WEIGHT = float(config.get("weights", "input"))
        OUTPUT_WEIGHT = float(config.get("weights", "output"))
        FINAL_WEIGHT = TID_WEIGHT + TACTIC_WEIGHT + TECHNIQUE_WEIGHT + INPUT_WEIGHT + OUTPUT_WEIGHT

        filepath = Path(config.get("paths","outputpath") + 'Alternatives.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df = pandas.read_csv(config.get("paths","knowledgebase"))
        attack = pandas.read_csv(config.get("paths","input"))
        out_dict = {}
        out_df = pandas.DataFrame()
        sep = '.'

        desired_confidence = (input("Enter desired confidence, from 0.0 to 1.0: "))
        desired_confidence = float(desired_confidence)

        for i in range(attack.shape[0]):
            df_string = "T" + str(i)
            out_dict[df_string] = [attack["TestId"][i]]
            out_dict[df_string + " confidence"] = [1.0]

            attackdata = df.loc[df['TestId'] == attack["TestId"][i]]
            attack_inputlist = attackdata["Input Type"].values[0]
            if (isinstance(attack_inputlist,str)):
                attack_inputlist = attack_inputlist.split('/')
            else:
                attack_inputlist = ["NONE"]
            
            attack_outputlist = attackdata["Output Type"].values[0]
            if (isinstance(attack_outputlist,str)):
                attack_outputlist = attack_outputlist.split('/')
            else:
                attack_outputlist = ["NONE"]   

            attack_system = attackdata["Supported Platform"].values[0]
            if (isinstance(attack_system,str)):
                attack_system = attack_system.split(',')
            else:
                attack_system = ["NONE"]  

            # Sanitize inputs for input/output by uppercasing them
            attack_inputlist = [x.upper() for x in attack_inputlist]
            attack_outputlist = [x.upper() for x in attack_outputlist]
            attack_system = [x.upper() for x in attack_system]

            for j in range(df.shape[0]):
                running_confidence = 0.0


                #look for exact match ID
                if(df["TestId"][j] == attackdata["TestId"].values[0]):
                    continue

                #Look for incompatble tests
                if (BYPASS_OS):
                    system = df["Supported Platform"][j]
                    if (isinstance(system,str)):
                        system = system.split(',')
                    else:
                        system = ["NONE"]
                    system = [x.upper() for x in system]
                    mismatch = list(set(attack_system) - set(system))
                    combined_count = len(attack_system) + len(system)
                    if (len(mismatch) > 0): #TODO: Fix in case of attack using Linux, but asks for Linux/MacOS
                        continue

                #look for partial match ID
                partial = df["TestId"][j].split(sep, 1)[0]
                if(partial == attackdata["TestId"].values[0].split(sep, 1)[0]):
                    #calculate confidence
                    running_confidence += TID_WEIGHT


                if(df["Tactic"][j].upper() == attackdata["Tactic"].values[0].upper()):
                    running_confidence += TACTIC_WEIGHT

                if(df["Technique"][j].upper() == attackdata["Technique"].values[0].upper()):
                    running_confidence += TECHNIQUE_WEIGHT

                inputlist = df["Input Type"][j]
                if (isinstance(inputlist,str)):
                    inputlist = inputlist.split('/')
                else:
                    inputlist = ["NONE"]

                outputlist = df["Output Type"][j]
                if (isinstance(outputlist,str)):
                    outputlist = outputlist.split('/')
                else:
                    outputlist = ["NONE"]
                    
                # Sanitize inputs for input/output by uppercasing them
                inputlist = [x.upper() for x in inputlist]
                outputlist = [x.upper() for x in outputlist]
                
                #Check Inputlist Matches
                mismatch = list(set(attack_inputlist) - set(inputlist))
                combined_count = len(attack_inputlist) + len(inputlist)
                running_confidence += (1 - len(mismatch) / combined_count)

                #Check Outputlist Matches
                mismatch = list(set(attack_outputlist) - set(outputlist))
                combined_count = len(attack_outputlist) + len(outputlist)
                running_confidence += (1 - len(mismatch) / combined_count)

                running_confidence /= FINAL_WEIGHT
                running_confidence = round(running_confidence,3)

                if (running_confidence >= desired_confidence):
                    out_dict[df_string].append(df["TestId"][j])
                    out_dict[df_string + " confidence"].append(running_confidence)

        out_df = pandas.DataFrame(dict([ (k,pandas.Series(v)) for k,v in out_dict.items() ]))
        #out_df = pandas.DataFrame.from_dict(out_dict)
                    
        out_df.to_csv(filepath, index=False)
        a = pandas.read_csv(config.get("paths","outputpath") + "Alternatives.csv")
        a.to_html(config.get("paths","outputpath") + "Alternatives.html")


        