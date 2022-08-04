import pandas as pd
import numpy as np

#Names: just a list with strings; Parents: Integer Array
def create_depth(Parents):
    depthlist = np.copy(Parents)
    depthlist[0] = 0
    for i in range(1,len(depthlist)):
        j= Parents[i]
        depthlist[i] = depthlist[j] + 1
    return depthlist

# Makes Header of BVH; Names: List of strings; Parents: int-array; length integer
def make_Header(Names, Parents, Offset, length, time= 0.01, chr = "  ", mode=3):
    Out = "HIERARCHY\n"
    depthlist = create_depth(Parents)
    lngth = Offset.shape[0]
    offst1 = "CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation"
    if mode == 6:
        offst = offst1
    else:
        offst =  "CHANNELS 3 Zrotation Xrotation Yrotation"

    def OSet(i):
        return " " + str(Offset[i][0]) + " " + str(Offset[i][1]) + " " + str(Offset[i][2])
    Out += "ROOT " + Names[0] + "\n{\n" + chr + "OFFSET" + OSet(0) +"\n"+ chr + offst1 + "\n"

    for i in range(1,lngth):
        d = depthlist[i]
        if (i==lngth-1) or (d>depthlist[i+1]):
            Out += d * chr + "End Site\n"
            Out += d * chr + "{\n"
            Out += (d+1) * chr + "OFFSET"
            Out += OSet(i) + "\n"
            # Zuklammern:
            if (i==lngth-1):
                d2=d - 1
            else:
                d2 = d - depthlist[i+1]
            for j in range(0,d2+1):
                Out += (d-j) * chr + "}\n"
        else:
            Out += d * chr + "JOINT " + Names[i] + "\n"
            Out += d * chr + "{\n"
            Out += (d+1) * chr + "OFFSET"
            Out += OSet(i) + "\n"
            Out += (d+1) * chr + offst + "\n"



    Out += "}\nMOTION\nFrames: " + str(length) + "\nFrame Time: " + str(time) + "\n"
    return Out

# Prints Root position and angles
def print_angles(Angles, length):
    OUT = ""
    length2 = Angles.shape[1]
    for i in range(length):
        LINE = ""
        for j in range(length2):
            LINE += str(Angles[i][j][0]) + " " + str(Angles[i][j][1]) + " " + str(Angles[i][j][2]) + " "
        if (i == (length-1)):
            OUT += LINE
        else:
            OUT += LINE + "\n"
    return OUT

# returns the entire BVH as a string
def print_BVH(Angles, Names, Parents, Offset, time= 0.01, chr = "  ", mode=3):
    length = Angles.shape[0]
    return make_Header(Names, Parents, Offset, length, time, chr, mode) + print_angles(Angles, length)
