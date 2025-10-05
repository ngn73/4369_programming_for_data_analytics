import csv
import os

FILENAME= "data.csv"
DATADIR = os.getcwd() + "\\"  # current directory
with open (DATADIR + FILENAME, "rt") as fp:
    reader = csv.reader(fp, delimiter=",")
    linecount = 0
    total_age = 0
    for line in reader:
        if not linecount: # first row ie header row
            print (f"{line}\n-------------------")
        else: # all subsequent rows
            print (line)
            total_age += int(line[1])
        linecount += 1
    print (f"average is {total_age/(linecount - 1)}")