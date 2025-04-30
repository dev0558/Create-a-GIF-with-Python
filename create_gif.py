from PIL import Image
import imageio.v3 as iio

# Resize both images to the same size
def resize_image(filename, size):
    img = Image.open(filename)
    img = img.resize(size)
    img.save(filename)

# Resize images to 512x512
resize_image("pic1.png", (512, 512))
resize_image("pic2.png", (512, 512))

# Now create the GIF
filenames = ['pic1.png', 'pic2.png']
images = [iio.imread(fname) for fname in filenames]
iio.imwrite('my_gif.gif', images, duration=500, loop=0)
