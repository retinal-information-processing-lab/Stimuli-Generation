import numpy as np

class StimuliGereration():


	def create_f_for_mea2: (x_pix, y_pix, fdim):
		# this function creates an F of the desired dimension

		# x_pix=1920
		# y_pix=1080
		background=np.zeros((x_pix, y_pix))
		center=[x_pix/2, y_pix/2]
		background[center[0],center[1]-fdim/2:center[1]+fdim/2 ]=255 
		background[center[0]: center[0]+fdim/3,center[1]+fdim/2]=255
		background[center[0]: center[0]+fdim/4,center[1]+fdim/3]=255

		return background
