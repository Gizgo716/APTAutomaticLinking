import pandas
import numpy

#Ask user for confidence value
#Ask user for database file
#Ask user for attack matrix

#Import the required Database files as db
#Import the attack matrix as a CSV as Attack

#Generate an output CSV with the number of attacks *2 as the number of columns. Infinite rows.
#Columns generate in this pattern:
    #S1, S1Conf, S2, S2Conf, S3, S3Conf ...

#ENTER LOOP
    #Load Technique from Attack Matrix as STEP

    # In a new 2D array, list possible techniques and their confidence values.
    #Start with the original with a confidence of 1.0.

    #Ask db for tactic in column.
    #First ask for exact match. First, get Subtechnique. If subtechnique does not exist, ask for technique.
        #If exact match is found, get tactic, input, outputs, technique
        #If only supertechnique is found, print a wanring, and use.
        #If not found, ignore the step. Print a warning message of not existing in database.

    #Once tactic, input and output is found, do a SQL style query for a match of all three. Fuzzy match, use LIKE not EQUALS.
        #We want if the input matches at least one of the required inputs
            #Original Technique needs Specific File, it should match onf Specific File/Information


    #First do a match for all three matching. Input Match, Output Match, Tactic Match. Technique is not used in matching.
    #Then drop tactic. Match Input, Output.

    #For each match
        #Calculate confidence value. Confidence starts at 0.0.
        #Each match is a .25 boost to confidence value.
        #Perfect match gets a confidence value of 1.0
            #This would be the original technique plus all inputs match exact, outputs match exact, tactic matches, technique.
        #Partial input match multiplies .25 by fraction of matches. For example, if Information matched with Information/File, this would be .5 * .25, resulting in .125 total confidence.

        #If calculated confidence is larger than user value:
                #Add the matched technique to the array of techniques. The next column is calculated confidence
    
    #Append the final array to the output CSV.
    
    #If there are no more techniques, exit loop.

#Export alternative matrix as CSV
