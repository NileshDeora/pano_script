from PIL import Image
import os

def compressImage():
    def compress_image(file_path, quality=85, max_size=(1500, 1500)):
        #Compress an individual image.
        img = Image.open(file_path)
        img.thumbnail(max_size, Image.ANTIALIAS)
        # new_width = img.width
        # new_height = img.height
        # reduce_width = int(new_width * 0.5)
        # reduce_height = int(new_height * 0.5)
        # print(reduce_width, reduce_height)
        # final_image = img.resize((reduce_width, reduce_height), Image.ANTIALIAS)
        # Save the compressed image, replacing the original
        img.save(file_path, 'png', quality=quality, optimize=True)

    def compress_images_in_folder(folder_path, quality=85, max_size=(1500, 1500)):
        """Compress all JPEG images in the specified folder."""
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.png'):
                file_path = os.path.join(folder_path, filename)
                print(f"Compressing {file_path}...")
                compress_image(file_path, quality, max_size)
                print(f"Finished compressing {file_path}")
        
        print("All images have been compressed and saved.")
        mergeImages()
    # Usage example
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    folder_path = parent_dir +'/output/results'
    print(folder_path)
    compress_images_in_folder(folder_path, quality=85)

def mergeImages():
    print("Merge images start, lets go")
    def create_image_grid(image_files, grid_size, image_size=(1500, 1500)):
        # Create a new image with the correct size
        grid_image = Image.new('RGB', (image_size[0] * grid_size[0], image_size[1] * grid_size[1]))
        # Load images and paste them into the grid image
        for index, file_path in enumerate(image_files):
            img = Image.open(file_path).resize(image_size)
            x = index % grid_size[0] * image_size[0]
            y = index // grid_size[0] * image_size[1]
            grid_image.paste(img, (x, y))
        
        return grid_image
    # old 12x12 (1,13)
    grid_size = (12, 12)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    image_paths = [f'{parent_dir}/output/results/row-{i}-column-{j}_rlt.png' for i in range(1, 13) for j in range(1, 13)]
    print(image_paths)
    # Create the grid image
    grid_image = create_image_grid(image_paths, grid_size)
    print("Merge Done")
    #for resizing image
    width = grid_image.width
    height = grid_image.height
    new_width = width
    new_height = width // 2  # Ensuring the ratio is 2:1
    image_2_1 = grid_image.resize((new_width, new_height), Image.ANTIALIAS)
    print("2:1 resize done")
    # Calculate half the size of the 2:1 resized image
    reduce_width = int(new_width * 0.75)
    reduce_height = int(new_height * 0.75)
    print("Resize to=>", reduce_width, reduce_height)
    # Resize the image to half of its current size
    final_image = image_2_1.resize((reduce_width, reduce_height), Image.ANTIALIAS)

    final_image.show()  # This will display the image grid in a window
    final_image.save(parent_dir +'/output/'+'merged_resize_compressed_img.png')  # Save the merged image
    print("Image merging + resize complete.")

def resizePano4k():
    print("resize works")
