import numpy as np

class StimuliGereration():
	
	def create_f(x_pix, y_pix, fdim, thick):
	    # this function creates an F of the desired dimension

	    background=np.zeros((x_pix, y_pix))
	    center=[int(y_pix/2), int(x_pix/2)]
	    background[center[1]-int(fdim/2):center[1]+int(fdim/2), center[0]-thick:center[0]+thick]=255 
	    background[center[1]+int(fdim/2)-thick:center[1]+int(fdim/2)+thick,center[0]:center[0]+int(fdim/3)]=255
	    background[center[1]+int(fdim/4)-thick:center[1]+int(fdim/4)+thick,center[0]:center[0]+int(fdim/5)]=255

	    return background

	def create_x(x_pix, y_pix, fdim, thick):
	    # this function creates a + cross of the desired dimension

	    background=np.zeros((x_pix, y_pix))
	    center=[int(y_pix/2), int(x_pix/2)]
	    background[:, center[0]-thick:center[0]+thick]=255
	    background[center[1]-thick:center[1]+thick,:]=255

	    return background
