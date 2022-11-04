# Import library from Image
from wand.image import Image

# Import the image
with Image(filename ='IWWS.jpeg') as image:
	# Clone the image in order to process
	with image.clone() as local_contrast:
        # radius is related to text size and picture size.
		# Invoke local_contrast function with radius 12 and sigma 3
		local_contrast.local_contrast(50, 90) # radius, sigma (0-100)
		# Save the image
		local_contrast.save(filename ='local_contrast1.jpg')
