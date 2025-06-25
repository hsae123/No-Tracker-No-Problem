import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ZScaleInterval

""" This simple script will save your final .fit(s) file into a PNG file.
Note that you may also save the image as a JPG, TIFF, or any other image file type.
A TIFF file will best preserve the detail and resolution of the original image, but will be large. A JPG will compress the file heaps and will result in a lower-quality image
A PNG is the better middle option between the two
"""

# 1. Load FITS data. This should be the final FITS data you are satisfied with
hdu_list = fits.open('final_color_stacked.fits')  # Replace 'final_color_stacked.fits' with your FITS file
data = hdu_list[0].data

# 2. Normalize data (if necessary)
# Check if normalization is needed
if data.dtype != 'uint8' and data.min() < 0 or data.max() > 255:
    # Normalize using ZScaleInterval
    interval = ZScaleInterval()
    normalized_data = interval.rescale(data)
    # Convert to uint8 if data type is not uint8
    if normalized_data.dtype != 'uint8':
        normalized_data = (normalized_data * 255).astype('uint8')
    # Use normalized_data instead of data
    data = normalized_data

# 3. Save as PNG (or any other imag extention)
plt.imshow(data, cmap='gray')  # Or use a different colormap
plt.axis('off')  
plt.savefig('output2.png', bbox_inches='tight', pad_inches=0)  # Save as PNG
plt.close()

# 4. Close the FITS file
hdu_list.close()
