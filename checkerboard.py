"""

A class to build the checkerboard stimulus.

Args:
    - nb_checks: the number of checks
    - binary_source_path: path to the binary source file
    - rig_nb: the set-up used for the experiments

"""

import os
from tqdm import tqdm
import numpy as np
import pickle

class Checkerboard:

    def __init__(self, nb_checks, binary_source_path, rig_nb):

        assert os.path.isfile(binary_source_path)

        self._nb_checks = nb_checks
        self._binary_source_path = binary_source_path
        self._rig_nb = rig_nb
        self._binary_source_file = open(self._binary_source_path, mode='rb')


    def __exit__(self, exc_type, exc_value, traceback):

        self._input_file.close()

        return

    def _get_bit(self, bit_nb):

        byte_nb = bit_nb // 8
        self._binary_source_file.seek(byte_nb)
        byte = self._binary_source_file.read(1)
        byte = int.from_bytes(byte, byteorder='big')
        bit = (byte & (1 << (bit_nb % 8))) >> (bit_nb % 8)

        return bit

    def get_image_shape(self):

        shape = (self._nb_checks, self._nb_checks)

        return shape

    def get_image(self, image_nb):
        """
        
        Create one checkerboard frame.

        Parameters
        ----------
        image_nb : int
            The frame number.

        Raises
        ------
        ValueError
            Bit value is not 0 or 1.

        Returns
        -------
        image : array
            Array containing 0 and 1 of dimension nb_checks x nb_checks.

        """

        shape = self.get_image_shape()
        image = np.zeros(shape, dtype=np.float)

        for i in range(0, self._nb_checks):
            for j in range(0, self._nb_checks):
                bit_nb = (self._nb_checks * self._nb_checks * image_nb) + (self._nb_checks * i) + j
                bit = self._get_bit(bit_nb)
                if bit == 0:
                    image[i, j] = 0.0
                elif bit == 1:
                    image[i, j] = 1.0
                else:
                    message = "Unexpected bit value: {}".format(bit)
                    raise ValueError(message)

        if self._rig_nb == 2:
            image = np.rot90(image)
            image = np.flipud(image)
            
        elif self._rig_nb == 3:
            image = np.fliplr(image)

        return image
    
    def build_checkerboard(self, nb_frames):
        """
        
        Creates the total checkerboard with nb_frames images.

        Parameters
        ----------
        nb_frames : int
            The total number of different checkerboard in the stimulation.

        Returns
        -------
        checkerboard_array : array of dimension nb_checks x nb_checks x nb_frames 
            An array containing all the frames.

        """
        checkerboard_array = np.ones((nb_frames,self._nb_checks,self._nb_checks), dtype='uint8') 
        for i in tqdm(range(checkerboard_array.shape[0]), desc="Reconstruction the stimulus"):
            checkerboard_array[i,:,:] = self.get_image(i)
        return checkerboard_array

    