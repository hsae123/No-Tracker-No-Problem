from astropy.io import fits
import numpy as np
import os
from skimage.registration import phase_cross_correlation
from scipy.ndimage import fourier_shift
import matplotlib.pyplot as plt
import cv2

"""
Please refer to README.md to better understand the thought process behind this program
"""

#  Step 1: Load raw Bayer images 
raw_images = []
file_list = sorted([f for f in os.listdir('../images') if f.endswith('.fit')]) # You may have .fit or .fits files depending on your camera hardware
# print(os.listdir())
for file in file_list:
    data = fits.getdata(file).astype(np.float32)
    raw_images.append(data)

#  Step 2: Align all raw Bayer images 
reference = raw_images[0]
aligned = []

for i, img in enumerate(raw_images):
    shift, error, diffphase = phase_cross_correlation(reference, img, upsample_factor=10)
    shifted = np.fft.ifftn(fourier_shift(np.fft.fftn(img), shift)).real
    aligned.append(shifted)

#  Step 3: Stack aligned raw images 
stacked_raw = np.median(np.stack(aligned), axis=0)

#  Step 4: Debayer stacked image 
stacked_raw = np.clip(stacked_raw, 0, 65535)
stacked_uint16 = stacked_raw.astype(np.uint16)

color_img = cv2.cvtColor(stacked_uint16, cv2.COLOR_BAYER_GB2RGB)
color_img = color_img.astype(np.float32)

#  Step 5: Stretch each channel 
for c in range(3):
    vmin = np.percentile(color_img[:, :, c], 1)
    vmax = np.percentile(color_img[:, :, c], 99)
    color_img[:, :, c] = np.clip((color_img[:, :, c] - vmin) / (vmax - vmin), 0, 1)

#  Step 6: Show and Save 
plt.imshow(color_img)
plt.title("Final Stacked Color Image")
plt.axis('off')
plt.show()

# Save as float32 FITS
hdu = fits.PrimaryHDU(color_img.astype(np.float32))
hdu.writeto("../output/final_color_stacked.fits", overwrite=True)
