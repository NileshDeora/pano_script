from PIL import Image
import os

# Increase the max pixel limit to handle very large images
Image.MAX_IMAGE_PIXELS = None  # This disables the decompression bomb check

def compress_png_image(input_image_path, output_image_path, compress_level=5, max_width=16384, max_height=8192):
    """
    Compresses very large PNG images (e.g., 24576x12288) while maintaining quality and transparency.

    Parameters:
    - input_image_path (str): Path to the original PNG image file
    - output_image_path (str): Path to save the compressed PNG image
    - compress_level (int): Compression level (0-9) for PNG (higher is smaller but slower)
    - max_width (int): Max width to resize the image (reduce this if needed)
    - max_height (int): Max height to resize the image (reduce this if needed)
    """

    # Open the original image
    img = Image.open(input_image_path)

    # Resize the image if it exceeds the max width/height while maintaining the aspect ratio
    img.thumbnail((max_width, max_height))

    # Save the image as PNG with specified compression level
    img.save(output_image_path, 'PNG', optimize=True, compress_level=compress_level)

    # Show before and after file sizes
    original_size = os.path.getsize(input_image_path) / (1024 * 1024)  # Convert to MB
    compressed_size = os.path.getsize(output_image_path) / (1024 * 1024)  # Convert to MB

    print(f"Original size: {original_size:.2f} MB")
    print(f"Compressed size: {compressed_size:.2f} MB")

# Example usage
input_image = "./results/7kNew.png"
output_image = "./results/path_to_compressed_image.png"
compress_png_image(input_image, output_image)
