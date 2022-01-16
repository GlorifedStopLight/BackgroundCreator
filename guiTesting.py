# Import required Image library
from PIL import Image, ImageFilter


# Open existing image
OriImage = Image.open('file_name.png')
OriImage.show()

# 300 no definition
# 100 some difference
# 50 original starts to show through
# 10 finer detail removed
# 2 shape of each dot is blurred into a solid line
# float or int allowed
blurImage = OriImage.filter(ImageFilter.GaussianBlur(radius=5))
blurImage.show()
# Save blurImage
# blurImage.save('file_name.png')