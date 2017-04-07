# very simple example of reading a gradebook JSON
# - reads in the JSON file and says how often each student was late
#   and what their avergae score was (using the robust "drop the lowest 2"
#   it puts its output to the console
#
#  - can be run from the command line
#       python exampleReader.py jsonfile.json
#
# sample code for CS765 Design Challenge 3
#
# this doesn't do a visualization (although, arguably it is a visualization)
# but it does show how to read in a data file and produce an output
# (in this case, text, not a picture)
#
# this is written using Python 3.6 - and as little extra stuff as possible
#   OK, I added numpy for mean, but everyone has numpy :-)
#
# you may use this as part of your own solution, but remember to provide properr
# attribution
#
# Mike Gleicher, April 2017

import json
import numpy
import sys

def gradebookSimple(filename):
    with open(filename,"rb") as fp:
        gb = json.load(fp)          # loads the json file

        numassigns = len(gb["assignments"])

        # iterate over the students...
        for student in gb["students"]:
            # make a list of the scores for all the assignments
            scores = [g["score"] for g in student["grades"]]
            # for the scores, drop the lowest 2
            scores.sort()
            scores = scores[2:]

            # for the late, don't consider anything that's less than 4 hours late late
            lates  = [g["late"]  for g in student["grades"] if g["late"]>=4]

            # just print out the info - but to make nice columns, limit the width to 30 characters
            print("{:>30} - score:{:5.2f} late:{:2d}/{:2d}".format(student["sortable_name"][:30],numpy.mean(scores),len(lates),numassigns))

# if this is run from the command line - call the program appropriately
# yes, I know this is a over-simplified way to do this, but it's meant to be quick and dirty
if __name__ == "__main__":
    gradebookSimple(sys.argv[1])
