import numpy as np
from scipy.spatial.transform import Rotation as RT

#Given an Offset and a vector finds a Rotation using Quaternions
def single_vec(o, v): #Assuming both non Zero
    a = np.copy(o)
    b = np.copy(v)
    help = np.zeros((4,), dtype= "float64")
    nsq_a = np.inner(a,a)
    nsq_b = np.inner(b,b)
    help[0:3] = np.cross(a, b)
    help[3] = np.sqrt(nsq_a * nsq_b) + np.inner(a,b)
    h_norm = np.linalg.norm(help)
    RotC = RT.from_quat(help/h_norm)
    return RotC.as_matrix()

#Finds Rotation between a vector pair 
def multi_vec(o1, o2, v1, v2): #Assuming all non Zero
    O1 = np.copy(o1)
    O2 = np.copy(o2)
    V1 = np.copy(v1)
    V2 = np.copy(v2)
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
    return G
  
