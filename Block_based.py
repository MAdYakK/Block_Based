import os
from PIL import Image, ImageOps
from collections import Counter


# Detect background color based on corner pixels and a few random pixels
def detect_background_color(img):
    
    width, height = img.size
    corners = [
        img.getpixel((0, 0)),
        img.getpixel((width - 1, 0)),
        img.getpixel((0, height - 1)),
        img.getpixel((width - 1, height - 1)),
    ]
    random_pixels = [
        img.getpixel((width // 4, height // 4)),
        img.getpixel((3 * width // 4, height // 4)),
        img.getpixel((width // 4, 3 * height // 4)),
        img.getpixel((3 * width // 4, 3 * height // 4)),
    ]
    corners.extend(random_pixels)
    background_color = Counter(corners).most_common(1)[0][0]
    return background_color

# Remove background color and replace it with transparency
def remove_background(image, background_color):
    
    image = image.convert("RGBA")
    datas = image.getdata()
    new_data = []
    for item in datas:
        if item[:3] == background_color or all(abs(item[i] - background_color[i]) < 5 for i in range(3)):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image
# Add grid lines around non-transparent pixels
def add_grid_lines_around_pixels(image, scale=9, pixel_size=8):
   
    original_width, original_height = image.size
    new_width = original_width * scale
    new_height = original_height * scale
    new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    for x in range(original_width):
        for y in range(original_height):
            pixel = image.getpixel((x, y))
            if pixel[3] != 0:
                for i in range(pixel_size):
                    for j in range(pixel_size):
                        if x * scale + i + 1 < new_width and y * scale + j + 1 < new_height:
                            new_img.putpixel((x * scale + i + 1, y * scale + j + 1), pixel)
                for i in range(pixel_size + 2):
                    if x * scale + i < new_width and y * scale < new_height:
                        new_img.putpixel((x * scale + i, y * scale), (0, 0, 0, 255))
                    if x * scale + i < new_width and y * scale + pixel_size + 1 < new_height:
                        new_img.putpixel((x * scale + i, y * scale + pixel_size + 1), (0, 0, 0, 255))
                for j in range(pixel_size + 2):
                    if x * scale < new_width and y * scale + j < new_height:
                        new_img.putpixel((x * scale, y * scale + j), (0, 0, 0, 255))
                    if x * scale + pixel_size + 1 < new_width and y * scale + j < new_height:
                        new_img.putpixel((x * scale + pixel_size + 1, y * scale + j), (0, 0, 0, 255))
    return new_img

# Merge foreground image with transparent pixels onto a background
def merge_with_background(foreground_img, background_color):
    
    new_width, new_height = foreground_img.size
    background_img = Image.new("RGBA", (new_width, new_height), background_color)
    background_img.paste(foreground_img, (0, 0), foreground_img)
    return background_img

# Ensure that any black lines or stray pixels on the background are removed
def final_background_cleanup(image, background_color):
  
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if pixel[3] == 0:
                pixels[x, y] = background_color + (255,)
    return image

def process_image(image_path, output_path, scale=9, pixel_size=8):
    img = Image.open(image_path).convert("RGBA")
    background_color = detect_background_color(img)
    print(f"Processing {os.path.basename(image_path)}: Detected background color: {background_color}")
    img_no_bg = remove_background(img, background_color)
    img_with_lines = add_grid_lines_around_pixels(img_no_bg, scale=scale, pixel_size=pixel_size)
    final_img = merge_with_background(img_with_lines, background_color)
    cleaned_img = final_background_cleanup(final_img, background_color)
    cleaned_img.save(output_path)

def process_folder(input_folder, output_folder, scale=9, pixel_size=8):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.png"
            output_path = os.path.join(output_folder, output_filename)
            process_image(input_path, output_path, scale, pixel_size)

# Example usage
process_folder("Images_to_process", "Processed", scale=9, pixel_size=8)
# modify all instances of scale='x'and pixel_size='x' to adjust scaling/outline thickness
