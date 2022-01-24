from tkinter import *
from PIL import ImageFilter, Image


# Open existing image
OriImage = Image.open('myImages/squid game marbles vibes.png')
OriImage.show()

# Applying GaussianBlur filter
gaussImage = OriImage.filter(ImageFilter.GaussianBlur(5))
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.EMBOSS())
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.CONTOUR())
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.EDGE_ENHANCE())
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.EDGE_ENHANCE_MORE())
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.FIND_EDGES())
gaussImage.show()

gaussImage = OriImage.filter(ImageFilter.MinFilter)
gaussImage.show()

# Save Gaussian Blur Image
# gaussImage.save('images/gaussian_blur.jpg')

