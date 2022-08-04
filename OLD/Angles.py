import numpy as np
from scipy.spatial.transform import Rotation as RT
from BVHMethods.Angle_make import Angles

# Maybe I shoud check whether scipy version is numerically more stable.
def R(angles): #Gives Back Rotationmatrix Inverse = Transposed for BHV; np.copy #Brauch man hier eigentlich nich unbedingt.
    angles *= 0.017453292519943295
    X = np.array([[1, 0, 0], [0, np.cos(angles[1]), -np.sin(angles[1])], [0, np.sin(angles[1]), np.cos(angles[1])]], dtype='float64')
    Y = np.array([ [np.cos(angles[2]), 0, np.sin(angles[2])], [0, 1, 0], [-np.sin(angles[2]), 0, np.cos(angles[2])]], dtype='float64')
    Z = np.array([[np.cos(angles[0]), -np.sin(angles[0]), 0], [np.sin(angles[0]), np.cos(angles[0]), 0], [0, 0, 1]], dtype='float64')
    return Z@X@Y

def find_Rot_M(Offset1, Offset2, Value1, Value2): #finds Rotation between two independent vectors and their respective Offest.
    O1 = np.copy(Offset1)
    O2 = np.copy(Offset2)
    V1 = np.copy(Value1)
    V2 = np.copy(Value2)
    #Basically Gram Schmidt:
    O2 -= (np.inner(O1,O2)/np.inner(O1, O1)) * np.copy(O1)
    O3 = np.cross(O1,O2)
    O1 /= np.linalg.norm(O1)
    O2 /= np.linalg.norm(O2)
    O3 /= np.linalg.norm(O3)
    
    V2 -= (np.inner(V1,V2)/np.inner(V1, V1)) * np.copy(V1)
    V3 = np.cross(V1,V2)
    V1 /= np.linalg.norm(V1)
    V2 /= np.linalg.norm(V2)
    V3 /= np.linalg.norm(V3)
    
    O = np.vstack((O1,O2,O3))
    V = np.vstack((V1,V2,V3))
    #return O,V
    G = V @ O.T
    RotM = RT.from_matrix(G)
    angles = RotM.as_euler('zxy', degrees = True)
    return G, angles

def find_Rot_S(Offset, Value): #finds Rotation between a single vector and its respective Offset. #Maybe change order if error occurs
    a = np.copy(Offset)
    b = np.copy(Value)
    help = np.zeros((4,), dtype= "float64")
    nsq_a = np.inner(a,a)
    nsq_b = np.inner(b,b)
    if (nsq_a == 0) or (nsq_b ==0):
        print("Quaternion is Zero. Division by Zero is not a good Idea")
        return help
    help[0:3] = np.cross(a, b)
    help[3] = np.sqrt(nsq_a * nsq_b) + np.inner(a,b)
    h_norm = np.linalg.norm(help)
    RotC = RT.from_quat(help/h_norm)
    return RotC.as_matrix(), RotC.as_euler('zxy', degrees = True)

#creates a single line
# V_Parent saves 
def make_line(Line, A_Parent, V_Parent, Offset, Use_multiple, A_items, Item_dict, AtoV):
    Matlist = np.zeros((A_items, 3,3), dtype = "float64")
    Angles = np.zeros((A_items,3),dtype = "float64")
    Matlist[0] = np.identity(3)
    Angles[0] = Line[0]
    for i in range(1,A_items):
        if Use_multiple[0] == True:
            # Search for correct Offset 
            Offset1 = np.copy(Offset[Item_dict[i][0]])
            Offset2 = np.copy(Offset[Item_dict[i][1]])
            #Apply Rotation of A_Parent to Offset; ;maybe Transpose
            Offset1 = Offset1 @ Matlist[A_Parent[i]]
            Offset2 = Offset2 @ Matlist[A_Parent[i]]
            
            # Goto would be good here... Alternative change i and alter Use_multiple, Should not happen though if I do use_multiple correctly
            # Search for correct entries for Value Vectors
            Value1 = Line[Item_dict[i][0]] - Line[V_Parent[i]]
            Value2 = Line[Item_dict[i][1]] - Line[V_Parent[i]]
            
            #Feed Variables into find_Rot_M 
            M, Angles[i] = find_Rot_M(Offset1, Offset2, Value1, Value2)
            Matlist[i] = Matlist[A_Parent] @ M
        else:
            #Do the same steps just for a single vector
            # Offset muss mit Matlist multipliziert werden!!!
            Offset1 = np.copy(Offset[AtoV[i][0]])
            Offset1 = Offset1 @ Matlist[A_Parent[i]]
            Value1 = Line[AtoV[i][0]] - Line[V_Parent[i]]
            M, Angles[i] = find_Rot_S(Offset1, Value1)
            Matlist[i] = Matlist[A_Parent[i]] @ M      
        #Thing about the last case where an offset is completely zero, but not the first one
    return Angles, Matlist


#def to_Angles(Lines, length, A_Parent, V_Parent, Offset, Use_multiple, A_items, Item_dict, AtoV):
 
def to_Angles(Lines, length, AngleClass):
    Angles = np.zeros((length,AngleClass.A_items,3), dtype="float64")
    for i in range(length):
    #for i in range(1):
        Angles[i], M = make_line(np.copy(Lines[i]), AngleClass.A_Parent, AngleClass.V_Parent, AngleClass.Offset, AngleClass.Use_multiple, AngleClass.A_items, AngleClass.Item_dict, AngleClass.AtoV)
        #if i ==0:
        #    print("Matrices: ",M)
    return Angles

"""
Lines         3-Tensor              Position data
length        Integer               Shape of first indices of Lines
A_Parent      Integer Array         Gives Angle Parent of i-th Angle element 
V_Parent      Integer Array         Gives Value Parent of i-th Angle element
Offset        2-Tensor              Gives Offset
Use_multiple  boolean Array         Tells whether bone has more than one vector
A_items       Integer               Number of Items 
Item_dict     Dict of int pairs     Relates multiple angles to their related Values
AtoV          Dict of integers      Relates a single angle to its related Value
"""