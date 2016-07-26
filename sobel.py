import numpy as np
import scipy.misc
import scipy.ndimage as ndimage

img = scipy.misc.imread('img.jpg', flatten=True)
sx = ndimage.sobel(img, axis=0, mode='constant')
sy = ndimage.sobel(img, axis=1, mode='constant')
filtered = 1 - np.hypot(sx, sy)
scipy.misc.imsave('filter.jpg', filtered)
