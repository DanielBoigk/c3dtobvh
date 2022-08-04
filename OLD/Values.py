# Works sofar, but quite slow.
import numpy as np
"""
def R(x,y,z): #Gives Back Rotationmatrix Inverse = Transposed for BHV
    X = np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]], dtype='float64')
    Y = np.array([ [np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]], dtype='float64')
    Z = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]], dtype='float64')
    return Z@X@Y

# Makes Rotationmatrix needed for further calculation
def make_RotM(angles):
    h = np.pi/180
    return R(angles[1]*h, angles[2]*h, angles[0]*h)
"""
# Maybe I shoud check whether scipy version is numerically more stable.
def make_RotM(angles): #Gives Back Rotationmatrix Inverse = Transposed for BHV; np.copy #Brauch man hier eigentlich nich unbedingt.
    #angles *= 0.01745
    angles *= 0.017453292519943295
    X = np.array([[1, 0, 0], [0, np.cos(angles[1]), -np.sin(angles[1])], [0, np.sin(angles[1]), np.cos(angles[1])]], dtype='float64')
    Y = np.array([ [np.cos(angles[2]), 0, np.sin(angles[2])], [0, 1, 0], [-np.sin(angles[2]), 0, np.cos(angles[2])]], dtype='float64')
    Z = np.array([[np.cos(angles[0]), -np.sin(angles[0]), 0], [np.sin(angles[0]), np.cos(angles[0]), 0], [0, 0, 1]], dtype='float64')
    return Z@X@Y

# Creates the Values for an entire Line
def make_line(Angles, Parents, Offset, Use_angl, V_items, A_items):
    Line = np.zeros((V_items, 3), dtype = "float64")
    Line[0] = Angles[0]
    MatList = np.zeros((V_items, 3, 3), dtype = "float64")
    MatList[0] = np.identity(3)
    for i in range(1,V_items):
        j = Parents[i]
        k = Use_angl[i]
        # Here some Matrix Multiplications could be avoided
        MatList[i] = MatList[j] @ make_RotM(Angles[k])
        Line[i] = Line[j] +  MatList[i] @ Offset[i]
    return Line

# 
def make_use(Parents, Depth, A_items, V_items):
    RA = np.zeros(V_items, dtype="int64")
    d_list = np.zeros(V_items, dtype="int64")
    d_count = 0
    for i in range(1,V_items):
        if Depth[i-1] < Depth[i]:
            d_list[Depth[i]] = i
            RA[i] = i -d_count
        else:
            RA[i] = d_list[Depth[i]]
            d_count += 1
            
    return RA
            

def to_Values(Angles, Parents, Offset, Depth, Frames, A_items, V_items, Use_angle):
    Values = np.zeros((Frames,V_items, 3), dtype="float64")
    #Use_angl = make_use(Parents, Depth, A_items, V_items)
    # Fill Use_angl correctly
    for i in range(Frames):
        Values[i] = make_line(Angles[i], Parents, Offset, Use_angle, V_items, A_items)
    
    return Values