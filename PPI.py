import numpy as np
import scipy.io as sio
import numpy.linalg as la
import matplotlib.pyplot as plt
from cvxopt import solvers, matrix

class PPI(object):

	data = None
	nRow = None
	nCol = None
	nBand = None
	nPixel = None
	p = None

	nSkewers = None
	initSkewers = None

	endmembers = None

	verbose = True

	def __init__(self, argin, verbose):
		self.verbose = verbose
		if (self.verbose):
			print ('---		Initializing PPI algorithm')
		self.data = argin[0].T
		self.nRow = argin[1]
		self.nCol = argin[2]
		self.nBand = argin[3]
		self.nPixel = argin[4]
		self.p = argin[5]

		self.nSkewers = argin[6]
		self.initSkewers = argin[7]

	def extract_endmember(self):
		if (self.verbose):
			print('---		Starting endmembers Extracting')

		M = self.data.T
		q = self.p
		numSkewers = self.nSkewers
		ini_skewers = self.initSkewers

		M = np.matrix(M, dtype=np.float32)
		p, N = M.shape
		u = np.transpose(np.transpose(M).mean(axis=0))
		Mm = M - np.kron(np.ones((1,N)), u)
		if ini_skewers == None:
			skewers = np.random.rand(p, numSkewers)
		else:
			skewers = ini_skewers
		votes = np.zeros((N, 1))
		if (self.verbose):
			print('---		Applying Projection to Skewers')
		for kk in range(numSkewers):
			tmp = abs(skewers[:,kk]*Mm)
			idx = np.argmax(tmp)
			votes[idx] = votes[idx] + 1
		max_idx = np.argsort(votes, axis=None)
		end_member_idx = max_idx[-q:][::-1]
		U = M[:, end_member_idx]
		if (self.verbose):
			print('---		Ending endmembers Extracting')
		
		self.endmembers = U
		return self.endmembers