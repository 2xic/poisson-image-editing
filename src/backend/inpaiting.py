from engine import image_handler, boundary
import numpy as np
from engine import poisson
from nptyping import Array

class inpaint(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a inpaited image.

	This contains all the functions needed to inpait a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	mode: str
	alpha: float

	def __init__(self, path: str, color: bool = False):
		if not path is None:
			image_handler.ImageHandler.__init__(self, path, color)
			boundary.Boundary.__init__(self, self.data.copy())
		else:
			boundary.Boundary.__init__(self)

		poisson.poisson.__init__(self)
		self.mask = None
		self.copy = None
		
	def set_data(self, data) -> None:
		"""
		Sets the data used by the class

		Parameters
		----------
		data : ndarray
			sets the data
		"""
		assert type(data) == np.array, "wrong argument"
		self.data = data

	def set_mask(self, mask) -> None:
		"""
		Sets the mask used by the class

		Parameters
		----------
		mask : ndarray
			sets the mask
		"""
		assert type(mask) == np.array, "wrong argument"
		self.mask = mask

	def set_orignal(self, original) -> None:
		"""
		Sets the original verison of the data(image) used by the class

		Parameters
		----------
		original : ndarray
			sets the original
		"""
		assert type(original) == np.array, "wrong argument"
		self.original_data_copy = original

	def destroy_information(self, strength=2, create_new_mask=False) -> Array:
		"""
		Removes parts of the image 
		
		Will also return a mask for the deleted parts of the image.

		Parameters
		----------
		strength : int
			a number from 1 to 10, this is used to set the level of noise added

		Returns
		-------
		array
			the image mask (where the data was removed)
		"""
		assert 0 <= strength and strength <= 10, "strength should be in the interval between 0 and 10"
		if self.mask is None or create_new_mask:
			noise = np.random.randint(0, 10, size=self.data.shape[:2])
			mask = np.zeros(self.data.shape[:2])

			mask[strength < noise] = 1
			mask[noise < strength] = 0
			self.mask = mask
		
		if(len(self.data.shape) == 3 ):
			for i in range(self.data.shape[-1]):
				 self.data[:, :, i] *= self.mask
		else:
			self.data *= self.mask
		self.original_data_copy = np.copy(self.data)
		return self.mask

	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""

		"""
		mask content
			original value = 1 
			infomation lost = 0 
		"""
		response = self.solve(self.data, self.operator, apply_boundary=False)
		
		# Update the values where the data has been lost
		if(len(self.data.shape) == 3):
			for i in range(self.data.shape[-1]):
				self.data[:, :, i] = (response[:, :, i] * (1 - self.mask)) + (self.original_data_copy[:, :, i] * (self.mask))
		else:
			self.data = (response * (1 - self.mask)) + (self.original_data_copy * (self.mask))
		
		self.data = self.diriclet(self.data, self.mask)
		return self.data

	def operator(self, i=None):
		"""
		Solves the "u" part of the poisson equation

		Returns
		-------
		array
			the u value
		"""
		if i is None:
			return self.get_laplace(self.data)	
		else:
			return self.get_laplace(self.data[:, :, i])

	def fit(self, original=None, data=None, mask=None, epochs:int=1) -> Array:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		original : ndarray
			The original version of the image
		data : ndarray
			Set current data (TODO : MAKE BETTER NAME)
		mask : ndarray
			Set mask of the image
		epochs : int
			The iteration count

		Returns
		-------
		array
			the new image array
		"""
		if not mask is None:
			self.set_mask(mask)
		if not original is None:
			self.set_orignal(original)
		if not data is None:
			self.set_data(data)
		if self.mask is None:
			raise Exception("You need to set a mask")

		for i in range(epochs):
			self.iteration()
		return self.data
