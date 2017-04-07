# simple example of making a visualization from a gradebook file
# designed to be as simple and minimal as possible - not a great visualization
#
# this turns a JSON file into an SVG file
# it uses svgwrite (a Python library for creating SVGs) -
#   svgwrite is not part of a regular Python install (you need to "pip install svgwrite"
# I don't know if svgwrite is any good, but I am trying it to learn about it
#
# the main thing here is to provide an example of how to deal with the data
# to read the data and do SOMETHING with it
# it is meant as a starting point so that students can make better things
#
# you are welcome to use this as a basis for your own projects - but remember to give
# proper attribution
#
# written by Mike Gleicher, April 2017
#

# extra libraries kept to a minimum since the goal is to make this easy
# but we need some stuff from the python standard library, and svgwrite
import json
import svgwrite
from typing import Tuple
import sys

# often in SVG we need to generate unique IDs for elements
global_id_counter = 0
def uniqid() -> str :
    """
    generate a unique ID for an SVG element
    :return: string
    """
    global global_id_counter
    global_id_counter += 1
    return "id-%d" % global_id_counter

# text is always a pain - since we never know what options and whatnot
# we also don't know how big it will end up being, or where it will actually go
# since the baseline may be something weird relative to the drawing position
# we put the text in a box and force a clipping rectangle to keep the text where
# we want it
# you still need to guess how big to make the box :-(
def textBox(drawing,string,fontsize=10,fontfamily="Arial",textanchor="start",
            textfill="black",
            insert=(0,0),
            boxxpad=5, boxypad=5, boxwidth=120, boxfill=None):
    # prevent the text from spilling too big by making a clip box
    clipid = uniqid()
    clip = drawing.clipPath(id=clipid)
    clip.add(drawing.rect((0,-boxypad-fontsize),(boxwidth,2*boxypad+fontsize)))

    # we need to style the text - otherwise, who knows what we'll get!
    style = ""
    style += "font-size:%dpx;"   % (fontsize)
    style += "font-family:%s;" % fontfamily
    style += "text-anchor:%s;" % textanchor
    text = drawing.text(string,style=style,fill=textfill)
    text["clip-path"]="url(#%s)"%clipid

    # put the text box into a group - that way we can draw the rectangle if necessary
    group = drawing.g()
    if boxfill:
        group.add(drawing.rect((-boxxpad,-boxypad-fontsize),(2*boxxpad+boxwidth,2*boxypad+fontsize),fill=boxfill))
    group.add(clip)
    group.add(text)
    group.translate((boxxpad+insert[0],boxypad+fontsize+insert[1]))

    return group

# color ramp - return an SVG color - but we need to start with tuples
def tupleToRGB(color : Tuple[int,int,int]) -> str:
    return '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))

# a simple "visualization" - write out a table of the scores - but color based on lateness
# bar chart on the number of postings - arranged vertically so you can compare within an assignment
def makeTable(gradebook, svgfilename):
    drawing = svgwrite.Drawing(svgfilename)
    for sn,student in enumerate(gradebook["students"]):
        sg = drawing.g()
        sg.add(textBox(drawing,student["sortable_name"]))
        left = 120 + 10 # boxwidth + 2*xpad
        for grade in student["grades"]:
            # make the width of the bar be the number of postings (max @ 5)
            nposts = min(5,len(grade["posts"]))
            sg.add(drawing.rect( (left,0),(nposts*5,15), fill="#CCC"))
            # write the score
            sg.add(textBox(drawing,"{:d}".format(grade["score"]),boxwidth=20,insert=(left,0),
                           textfill="#C00" if grade["late"]>=4 else "black"
                           ))
            left += 20 + 10 # boxwidth + 2*xpad
        sg.translate( (5,sn*20) )       # fontsize + 2*ypad
        drawing.add(sg)
    drawing.save(True)


if __name__ == "__main__":
    jsonFile = sys.argv[1]
    if jsonFile[-5:].upper() == ".JSON":
        with open(jsonFile,"rb") as fp:
            gradebook = json.load(fp)
            svgfile = jsonFile[:-5]+".svg"
            makeTable(gradebook,svgfile)
            print("Wrote SVG file {}".format(svgfile))
    else:
        print("Need a JSON file!")
