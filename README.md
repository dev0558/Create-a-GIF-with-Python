# Image to GIF Creator

A Python utility that converts multiple PNG images into an animated GIF with automatic resizing to ensure uniform dimensions.

## Features

- Automatically resizes multiple images to the same dimensions
- Creates smooth animated GIFs from image sequences
- Configurable animation speed and loop settings
- Simple and easy-to-use interface

## Requirements

- Python 3.x
- Pillow (PIL Fork)
- imageio

## Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/image-to-gif-creator.git
cd image-to-gif-creator

# Install dependencies
pip install pillow imageio
```

## Usage

1. Place your PNG images in the project directory
2. Modify the image filenames in the script if needed
3. Run the script:

```bash
python create_gif.py
```

The script will:
1. Resize all images to 512x512 pixels
2. Create an animated GIF named 'my_gif.gif'

## Customization

You can easily modify the script to:
- Change the target size by modifying the dimensions in the `resize_image()` function
- Adjust animation speed by changing the `duration` parameter (in milliseconds)
- Add more images by updating the `filenames` list

## Code

```python
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
```

## Future Improvements

- Add command-line arguments for more flexible usage
- Support for more image formats (JPEG, WebP, etc.)
- GUI interface for easier operation
- Option to preserve aspect ratio during resizing

