"""
This code works in principle, but it's quite slow. The reason I can't just use
numba to speed it up is the call of scipy. Maybe I should write it again using
Julia or C++. Or I can implement the scipy function in pure python myself.
"""

import numpy as np
from scipy.spatial.transform import Rotation

# Finds the Quaternion that rotates in between two vectors.
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

def R(x,y,z): #Gives Back Rotationmatrix Inverse = Transposed for BHV
    X = np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]], dtype='float64')
    Y = np.array([ [np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]], dtype='float64')
    Z = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]], dtype='float64')
    return Z@X@Y

# Returns Euler Angle of the Quaternion between two vectors.
def find_angle(Offset, Rel_Pos):
    quat = find_quat(Offset, Rel_Pos)
    #print("quat:", quat)
    R = Rotation.from_quat(quat)
    #return R.as_matrix(), R.as_euler('zxy', degrees= True)
    return R.as_euler('zxy', degrees= True)

#Constructs Rotationmatrix after BVH Standard for given angles
def make_RotM(angles):
    h = np.pi/180
    return R(angles[1]*h, angles[2]*h, angles[0]*h)

#Constructs Rotationmatrix and angles for two Points
def next_step (Rel_Pos, Offset, Prev_Matrix):
    angles = find_angle(Offset, Prev_Matrix.T @ Rel_Pos)
    NMatrix = Prev_Matrix @ make_RotM(angles)
    return angles, NMatrix

#Constructs angles of an entire line
def make_line(PosList , Offset, Parent, length):
    M = np.zeros((length,3,3))
    M[0] = np.identity(3)
    Angles = np.copy(PosList)
    a = PosList[2]
    b = PosList[1]
    for i in range(1,length):
        j = Parent[i]
        vec = PosList[i] - PosList[j]
        angl , A = next_step(vec, Offset[i], M[j])
        M[i]= A
        Angles[i] = angl
    return Angles

# Positions as Numpy 3-tensor, Offset as numpy 2-Tensor Parent as 1-Tensor
def Angles(Positions, Offset, Parent):
    dims = Positions.shape
    print(dims)
    BVH_angles = np.zeros(dims,dtype="float64")
    for k in range(dims[0]):
        BVH_angles[k] = make_line(Positions[k], Offset, Parent, dims[1])
    return BVH_angles
