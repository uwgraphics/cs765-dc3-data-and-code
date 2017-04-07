# store the information about a gradebook required for the class project
# this is a distilled set of information - designed to be easy to give to students for the Design Challenge
# and to be generated easily
#
# some design decisions:
#  only the data used in the Design Challenge Assignment is stored
#  things are kept in a "pre-joined" form
#  rather than a class, it's a dictionary - so it is more like JavaScript and can be sensibly jsonified
#  things are kept in lists, in order
#
#
# The schema:
# gradebook {
#   assignments : list of assignments {
#       "name" : string,
#       "id" : int                  (canvas ID number)
#               (other info not included since it's too hard to create randomly in test data)
#   },
#   students : list of students {
#       "sortable_name" : string,
#       "id" : integer,             (canvas ID number)
#               (other info not included since it's too hard to create randomly in test data)
#       "grades" : list of grades - same length of assignments list, in same order as assignments list {
#           "score" : int,      (assigned graded score - might be "None" if not graded, or 0 if not turned in
#           "late"  : int,      (number of HOURS late - negative means before the deadline, but might be 0)
#           "posts" : list of posting information {  (not tuples since I might add info later)
#               "length" : int, (post length in characters (after HTML removed))
#               "images" : int (number of images)
#           }
#       }
#   }
# }

import json
import csv
import random

def createDummyGradebook(nstudents=5, nassign=5, npost=3):
    """
    Create a totally silly gradebook - everyone gets the same score - mainly for testing
    :param nstudents: 
    :param nassign: 
    :param npost: 
    :return: a gradebook "object" (dictionary)
    """
    students = []
    for st in range(nstudents):
        assigns = []
        for na in range(nassign):
            assigns.append({"score":50, "late":0, "posts": [{"length":500,"images":1} for p in range(npost)]})
        students.append({"sortable_name":"Student, Alfred","id":1000+st,"grades":assigns})

    return {
        "assignments" : ["Assignment {}".format(i) for i in range(nassign)],
        "students" : students
    }


def writeGradebookCSV(filename,gradebook):
    """
    Write out as a "simple" CSV file - turns structs into tuples so they print more easily
    :param filename: 
    :param gradebook: 
    :return: 
    """
    with open(filename,"w") as fo:
        wr = csv.writer(fo,lineterminator="\n")
        # header row
        wr.writerow([ "sortable_name","id"] + gradebook["assignments"])
        # write each student row
        for st in gradebook["students"]:
            sr = [st["sortable_name"],st["id"]]
            sp = [ (g["score"],g["late"],[(p["length"],p["images"]) for p in g["posts"]]) for g in st["grades"]]
            wr.writerow(sr+sp)

def writeGradebookJSON(filename,gradebook):
    """
    write a simple json out
    :param filename: 
    :param gradebook: 
    :return: 
    """
    with open(filename,"w") as fo:
        json.dump(gradebook,fo,indent=4)

# generate a random thing from a range - skew good students upwards, and bad students downwards
def randomRange(range,good):
    p1 = random.randint(range[0],range[1])
    p2 = random.randint(range[0],range[1])
    if good:
        return max(p1,p2)
    else:
        return min(p1,p2)

# better random generators
def randomGradebook(nstudents:int = 5, assigns=5):
    # read in the list of random names - make them in sortable form
    # in fact, sort them - just because it makes things nicer
    names = [l.split(" ") for l in open("random_names.txt")]
    names = ["{}, {}".format(l[1],l[0]) for l in names if len(l)>1]
    random.shuffle(names)
    names = names[:nstudents]
    names.sort()
    # if you pass a list of assignment names, use them, otherwise, convert to a list of names
    if type(assigns)!=list:
        assigns = ["Discussion {}".format(i+1) for i in range(assigns)]
    # generate id numbers
    ids = set()
    while len(ids) < nstudents:
        ids.add(random.randint(1001,8999))
    ids = list(ids)

    # for each assignment, create it's defaults
    assignDescript = [(random.choice([(1,1),(1,3),(1,5),(2,5)]), # number of posts
                       random.choice([(200,800),(700,1300),(700,1300),(1000,2500)]), # length of first post
                       random.choice([(100,200),(100,300),(200,400)]), # length of subsequent posts
                       random.choice([(0,1),(0,2),(1,2)]) # images in first post
                       ) for a in range(len(assigns))]


    # now, generate grades for each student
    students = []
    for si in range(nstudents):
        name = names[si]
        id = ids[si]
        # decide if this is a good student or not
        good = random.choice([True,True,False])
        # generate a list of grades - one for each assignment
        grades = []
        for ad in assignDescript:
            score = random.choice([50,50,50,40,40,30] if good else [40,40,30,30,20])
            late = random.random() < .25
            lateness = random.randint(4,72) if late else random.randint(-48,-4)
            if lateness>12:
                score -= 5
            posts = [ {"length":randomRange(ad[1],good),"images":randomRange(ad[3],good)} ]
            for i in range(randomRange(ad[0],good)-1):
                posts.append({"length":randomRange(ad[2],good),"images":0})
            grades.append({"score":score,"late":lateness,"posts":posts})
        students.append({"sortable_name":name, "id":id,"grades":grades})

    return { "assignments":assigns, "students":students}