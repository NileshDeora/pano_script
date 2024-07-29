import requests
from PIL import Image
from io import BytesIO
import os
def make_grid():
    import omni.kit.pipapi
    omni.kit.pipapi.install("PIL")
    print('grid works', Image)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    parent_dir = os.path.dirname(parent_dir)+'\parallax_output'

    # file_name = outdata["name"]
    
    urls = [
        # "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1507_6751_1_1712579567797.png",
        # "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1512_6773_2_1713267279175.png",
        # "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1512_6772_2_1713267049464.png",
        # "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1516_6796_2_1715678875366.png",
        # "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1516_6797_2_1715678888975.png"
    ]
    walls = ['left', 'right', 'back', 'floor', 'ceiling']
    for wall in walls:
        urls.append(parent_dir+'\\'+wall+'.png')  
    
    data = []
    # for url in urls:
    #     print(url)
    #     response = requests.get(url)
    #     image = Image.open(BytesIO(response.content))  # Open the image from the in-memory bytes buffer
    #     data.append(image)
    for url in urls:
        image = Image.open(url)
        data.append(image)
    # Define grid parameters
    print('data is heree', data)
    output_size = 2160  # Size of the grid
    rows = [0.2667, 0.2667, 0.2667, 0.2]  # Row heights as fractions of total height (80% and 20% distribution)
    columns = [[1], [1], [1], [0.5, 0.5]]  # Column widths as fractions within each row

    # Create a new image for the grid
    grid = Image.new('RGB', (output_size, output_size))

    # Variables to track the y-coordinate and the height of the current row
    y_offset = 0

    # Place each image in its grid cell
    for i, (row_height, col_widths) in enumerate(zip(rows, columns)):
        row_pixel_height = int(output_size * row_height)
        x_offset = 0
        
        for j, col_width in enumerate(col_widths):
            col_pixel_width = int(output_size * col_width)
            
            # Select the image
            image = data.pop(0)
            aspect_ratio = image.width / image.height
            new_height = row_pixel_height
            new_width = int(aspect_ratio * new_height)
            
            if new_width > col_pixel_width:
                new_width = col_pixel_width
                new_height = int(new_width / aspect_ratio)
            
            # Resize the image
            resized_image = image.resize((new_width, new_height))
            
            # Calculate center position
            x_center = x_offset + (col_pixel_width - new_width) // 2
            y_center = y_offset + (row_pixel_height - new_height) // 2
            
            # Paste the resized image onto the grid
            grid.paste(resized_image, (x_center, y_center))
            
            # Move to the next column
            x_offset += col_pixel_width
        
        # Move to the next row
        y_offset += row_pixel_height

    # Save the final grid
    grid.save(r"C:\Users\NEIL\Downloads\Omni learning\headless_microservice_pano\pano_headless\exts\pano_headless\pano_headless\parallax_output\out3.png")
