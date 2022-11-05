# Import library from Image
from wand.image import Image

# Import the image
# 2160x1080
# the original image scale.

with Image(filename ='IWWS.jpeg') as image:
	# Clone the image in order to process
	with image.clone() as local_contrast:
        # radius is related to text size and picture size.
		# Invoke local_contrast function with radius 12 and sigma 3
		local_contrast.local_contrast(4, 150) # radius, sigma
		# Save the image
		local_contrast.save(filename ='local_contrast1.jpg')
		local_contrast.local_contrast(8, 75) # radius, sigma
		local_contrast.local_contrast(12, 75) # radius, sigma
		local_contrast.save(filename ='local_contrast2.jpg')