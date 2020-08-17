#######
# The purpose of this module is to provide utilities that make
# manipulating datafiles easier.
import pandas as pd
import numpy as np

def describeDatafile(inFilename, fileType = 'csv'):
    '''
    This function opens a datafile with the name given in "inFilename",
    reads its data into a two-column pandas dataframe in which the first
    column is the sequence and the second column is the genome type label
    (an integer). It then computes and returns a dictionary with statistics
    that describe the data in the data file.

    Input:
        - the name of the file to open
        - the type of file to handle (default is "csv"). Currently can only
            handle csv files. [.faa format should be added]

    Output:
        a dictionary that has the following key names (which provide the information
        described below):
            - validFlag: A boolean indicating whether the datafile was
                successfully read; Reasons for being false are: the data
                file having the wrong number of columns, the file not being
                found in the location indicated.
                [Add more as code to handle other reasons is written]
            - numRows: The number of rows in the data file (int)
            - allLetters: A list of each unique letter found in the file
                sequences
            - totalNumLetters: The total number of letters in the file (int)
            - avgLettsPerSeq: The average number of letters per sequence (float)
            - medLettsPerSeq: The median number of letters per sequnce (float)
            - maxLettsPerSeq: The maximum number of letters in a sequence (int)
            - minLettsPerSeq: The minimum number of letters in a sequence (int)
            - lettsInLine: A numpy array, the nth entry of which contains the
                number of letters that are in the nth row of the file (int)
            - naFirstCol: list of the row numbers where the first column value is NA
            - naSecCol: list of the row numbers where the second column value is NA

    '''
    outDict = {}

    try:
        df = pd.read_csv(inFilename, header=None, names = ["idx", "seq"])
    except:
        outDict["validFlag"] = False
        return outDict

    #DF without NaN rows:
    cleanDF = df[~df.seq.isna()]

    #one ~very~ long string of all the letters in all the rows:
    wholeStr = ''.join(cleanDF.seq.to_list())

    #to get list of which letters appear in each set of 3,000,000 rows...
    #break it up into batches, bc all at once, it's too long
    batchSize = 3000000
    #ERROR MESSAGE: name 'stepNum' is not defined (next row)
    letters = np.unique(np.array(list(wholeStr[stepNum*batchSize:(stepNum+1)*batchSize])))
    #to get the last few rows:
    lettersLast = np.unique(np.array(list(wholeStr[(len(wholeStr)//stepSize)*stepSize:])))
    #concatenate it all together:
    allLetters = np.concatenate([letters, lettersLast])
    #get the unique letters in the whole file:
    uniqueLetters = np.unique(np.concatenate(allLetters))

    outDict["validFlag"] = True
    outDict["numRows"] = df.shape[0]
    outDict["allLetters"] = uniqueLetters
    return(outDict)

if __name__ == "__main__":
    print("Hello, World!")
    inFilename = "/Users/Aidia/Documents/SummerResearch2020/NeuralNetData/test.csv"
    outDict = describeDatafile(inFilename)
    print(outDict)
