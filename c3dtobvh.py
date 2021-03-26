from ezc3d import c3d
import numpy as np
import matplotlib.pyplot as plt
import math

from numba import jit
from scipy.interpolate import interp1d

class C3D:
	def __init__(self, path):
		self.path =path
		self.c = c3d()
		self.c = c3d(self.path)
		self.point_data = self.c['data']['points']
		self.points_residuals = self.c['data']['meta_points']['residuals']
		self.analog_data = self.c['data']['analogs']
		self.labels = self.c['parameters']['POINT']['LABELS']['value']

		self.length = self.point_data[0][0,:].shape[0]
		self.T = np.arange(0, self.length)
		self.frequency = 250

		self.BVHTop = ''
		self.BVHDict = {}
		self.Channeldict = {}
		self.Offset_dict = {}

		self.BVH_means = {}
		self.BVH_variance = {}
		self.BVH_locale = {}
		self.BVH_Data = {}

	def clmn (self, name):	#Returns values of a given label as numpy array
		indx = self.c['parameters']['POINT']['LABELS']['value'].index(name)
		return np.vstack((self.point_data[0][indx,:], self.point_data[1][indx,:], self.point_data[2][indx,:]))
	
