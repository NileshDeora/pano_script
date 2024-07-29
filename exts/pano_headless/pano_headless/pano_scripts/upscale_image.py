import asyncio
from .merge_images import * 
import subprocess
from PIL import Image

def resize(path):
    with Image.open(path) as img:
        # Resize the image
        resized_img = img.resize((2880, 1620))
        width = resized_img.width
        height = resized_img.height
        new_width = width
        new_height = width // 2  # Ensuring the ratio is 2:1
        image_2_1 = resized_img.resize((new_width, new_height), Image.ANTIALIAS)
        print("2:1 resize done")
        # Save the resized image
        image_2_1.save(path)


    print(f"Image resized to 4k and saved.")
    upscale()
    

async def upscale_img():
    print("Upscaling render..")
    # Define the command and arguments
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    upscale_proj_path = parent_dir +'/upscale_model/upscale/'
    realesrgan_path = upscale_proj_path + "realesrgan-ncnn-vulkan.exe" 
    command = [
        realesrgan_path,
        "-i", upscale_proj_path+"media/",
        "-o", upscale_proj_path+"results/",
        "-n", "realesrgan-x4plus-anime",
        "-s", "4"
    ]
    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
    # Print the output and error (if any)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    print("upscale done")   


def upscale():
    asyncio.ensure_future(upscale_img())



