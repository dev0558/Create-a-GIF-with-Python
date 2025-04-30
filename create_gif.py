#!/usr/bin/env python3
"""
Image to GIF Creator

A Python utility that converts multiple PNG images into an animated GIF
with automatic resizing to ensure uniform dimensions.
"""

import os
import argparse
from PIL import Image
import imageio.v3 as iio


def resize_image(filename, size, output_dir=None, preserve_aspect_ratio=False):
    """
    Resize an image to the specified size.
    
    Args:
        filename (str): Path to the image file
        size (tuple): Target size as (width, height)
        output_dir (str, optional): Directory to save the resized image
        preserve_aspect_ratio (bool): Whether to preserve aspect ratio
    
    Returns:
        str: Path to the resized image
    """
    img = Image.open(filename)
    
    if preserve_aspect_ratio:
        # Calculate dimensions preserving aspect ratio
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        
        if img_width > img_height:
            new_width = size[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = size[1]
            new_width = int(new_height * aspect_ratio)
            
        # Create a new image with the target size
        new_img = Image.new("RGBA", size, (255, 255, 255, 0))
        
        # Resize the original image
        resized_img = img.resize((new_width, new_height))
        
        # Calculate position to paste (center)
        paste_x = (size[0] - new_width) // 2
        paste_y = (size[1] - new_height) // 2
        
        # Paste the resized image onto the new image
        new_img.paste(resized_img, (paste_x, paste_y))
        img = new_img
    else:
        # Simple resize to target dimensions
        img = img.resize(size)
    
    # Save the resized image
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(filename))
    else:
        output_path = filename
        
    img.save(output_path)
    return output_path


def create_gif(image_files, output_file, duration=500, loop=0, resize=None, preserve_aspect_ratio=False):
    """
    Create a GIF from a list of image files.
    
    Args:
        image_files (list): List of image file paths
        output_file (str): Output GIF file path
        duration (int): Frame duration in milliseconds
        loop (int): Number of times to loop (0 = infinite)
        resize (tuple, optional): Size to resize images to as (width, height)
        preserve_aspect_ratio (bool): Whether to preserve aspect ratio when resizing
    """
    # Create temporary directory for resized images
    temp_dir = "temp_resized"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Resize images if needed
    if resize:
        resized_files = [
            resize_image(img, resize, temp_dir, preserve_aspect_ratio) 
            for img in image_files
        ]
    else:
        resized_files = image_files
    
    # Read images
    images = [iio.imread(fname) for fname in resized_files]
    
    # Write GIF
    iio.imwrite(output_file, images, duration=duration, loop=loop)
    
    # Clean up temporary files if they were created
    if resize:
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
    
    print(f"GIF created successfully: {output_file}")


def main():
    """Main function to parse arguments and create GIF."""
    parser = argparse.ArgumentParser(description="Convert images to an animated GIF.")
    parser.add_argument("images", nargs="+", help="Image files to include in the GIF")
    parser.add_argument("--output", "-o", default="output.gif", help="Output GIF filename")
    parser.add_argument("--duration", "-d", type=int, default=500, help="Frame duration in milliseconds")
    parser.add_argument("--loop", "-l", type=int, default=0, help="Number of times to loop (0 = infinite)")
    parser.add_argument("--size", "-s", type=int, nargs=2, help="Resize images to WIDTH HEIGHT")
    parser.add_argument("--preserve-ratio", "-p", action="store_true", help="Preserve aspect ratio when resizing")
    
    args = parser.parse_args()
    
    size = tuple(args.size) if args.size else None
    
    create_gif(
        args.images,
        args.output,
        args.duration,
        args.loop,
        size,
        args.preserve_ratio
    )


if __name__ == "__main__":
    main()
