import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ZScaleInterval

# 1. Load FITS data
hdu_list = fits.open('final_color_stacked.fits')  # Replace 'your_file.fits' with your FITS file
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

# 3. Save as JPEG
plt.imshow(data, cmap='gray')  # Or use a different colormap
plt.axis('off')  # Remove axes
plt.savefig('output2.png', bbox_inches='tight', pad_inches=0)  # Save as JPEG
plt.close()  # Close the figure to release memory

# 4. Close the FITS file
hdu_list.close()