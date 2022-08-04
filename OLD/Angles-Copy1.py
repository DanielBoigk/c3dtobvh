import numpy as np
from scipy.spatial.transform import Rotation as RT

def R(x,y,z): #Gives Back Rotationmatrix Inverse = Transposed for BHV
    X = np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]], dtype='float64')
    Y = np.array([ [np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]], dtype='float64')
    Z = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]], dtype='float64')
    return Z@X@Y

# Makes Rotationmatrix needed for further calculation
def make_RotM(angles):
    h = np.pi/180
    return R(angles[1]*h, angles[2]*h, angles[0]*h)

def just_Test():
    print("Test Successful")

# Constructs an orthonormal Matrix via Gram Schmidt of Value and Offset vectors and finds Rotation matrix beetween the two.
def find_Rot_M(Offset1, Offset2, Value1, Value2):
    Offset2 -= (np.inner(Offset1,Offset2)/np.inner(Offset1, Offset1)) * Offset1
    Offset3 = np.cross(Offset1,Offset2)
    Offset1 /= np.linalg.norm(Offset1)
    Offset2 /= np.linalg.norm(Offset2)
    Offset3 /= np.linalg.norm(Offset3)
    
    Value2 -= (np.inner(Value1,Value2)/np.inner(Value1, Value1)) * Value1
    Value3 = np.cross(Value1,Value2)
    Value1 /= np.linalg.norm(Value1)
    Value2 /= np.linalg.norm(Value2)
    value3 /= np.linalg.norm(Value3)
    
    O = np.hstack((Offset1,Offset2,Offset3))
    V = np.hstack((Value1,Value2,Value3))
    RotM = V @ O.T
    RotC = RT.from_dcm(RotM)
    return RotM, RotC.as_euler('zxy', degrees = True)

# Finds a quaternion that portrais Rotation between 
def find_quat(a,b):
    help = np.zeros((4,), dtype= "float64")
    nsq_a = np.inner(a,a)
    nsq_b = np.inner(b,b)
    if (nsq_a == 0) or (nsq_b ==0):
        print("Quaternion is Zero. Division by Zero is not a good Idea")
        return help
    help[0:3] = np.cross(a, b)
    help[3] = np.sqrt(nsq_a * nsq_b) + np.inner(a,b)
    h_norm = np.linalg.norm(help)
    return help/h_norm

#Constructs Rotationmatrix between Offset and Value vector 
def find_Rot_S(Offset, Value):
    h = np.pi/180
    RotC = RT.from_quat(find_quat(Offset,Value))
    angles = RotC.as_euler()
    return R(angles[1]*h, angles[2]*h, angles[0]*h), angles
    

def make_line(InLine, Parents, Offset, Depth, A_items, V_items, Use_Angle, Angle_dict, Use_Multiple, h_dict):
    OutLine = np.zeros((A_items, 3), dtype = "float64")
    print("InLine: ", InLine.shape)
    print("Parents: ", Parents.shape)
    print("Offset: ", Offset.shape)
    print("Depth: ", Depth.shape)
    print("A_items: ", A_items)
    print("V_items: ", V_items)
    print("Use_Angle: ", Use_Angle.shape)
    print("Angle_dict: ", len(Angle_dict))
    print("Use_Multiple: ", Use_Multiple.shape)
    print(Angle_dict)
    Mat_List = np.zeros((A_items,3,3), dtype= "float64")
    Mat_List[0] = np.identity(3)
    for i in range(A_items):
        print(i, Angle_dict[i])

    return OutLine 

# Creates a dictionary that contains information about which values to use in case an angle corresponds to more than one value. 
def make_h_dict(Offset, A_items,V_items, Use_Angle, Use_Multiple, Angle_dict):
    h_dict = {}
    V =  np.zeros((2,3),dtype = "float64")
    I = np.zeros((2),dtype = "int64")
    for i in range(A_items):
        if Use_Multiple[i]: # Assuming vectors are not zero
            print(Angle_dict[i])
            l = len(Angle_dict[i])
            M= np.zeros((l,3),dtype="float64")
            M =  Offset[Angle_dict[i]]
            rk = np.linalg.matrix_rank(M)
            if rk <=1:
                Use_Multiple[i] = False # Careful! There could be the case where the first Offset is Zero, which could lead to division by zero.
            print(M)
            it = True
            for j in range(l):
                V[0] = M[j]
                for k in range(j,l):
                    V[1] = M[k]
                    if np.linalg.matrix_rank(V) == 2:
                        I[0] = j
                        I[1] = k
                        it = False
                        break
                if it == False:
                    break
            h_dict[i] = [I, V]
    return h_dict
    
def make_calc_dict(Parents, A_items, V_items, Use_Angle):
    
    print("To be implemented")
    return

def to_Angles(Values, Parents, Offset, Depth, Frames, A_items, V_items, Use_Angle, Angle_dict, Use_Multiple):
    # Creates a dictionary that contains information about which values to use in case an angle corresponds to more than one value. 
    h_dict = make_h_dict(Offset, A_items,V_items, Use_Angle, Use_Multiple, Angle_dict)

    print("h_dict: ",h_dict)        
    # A dictionary that contains information about which Angle to calculate in which order 
    A_Parent = make_calc_dict(Parents, A_items, V_items, Use_Angle)
    
    Angles = np.zeros((Frames,A_items,3), dtype = "float64")
    for i in range(1):
    #for i in range(0, Frames):
        Angles[i] = make_line(Values[i], Parents, Offset, Depth, A_items, V_items, Use_Angle, Angle_dict, Use_Multiple, h_dict)
    return Angles