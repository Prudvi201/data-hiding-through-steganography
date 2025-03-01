Python 3.12.8 (tags/v3.12.8:2dc476b, Dec  3 2024, 19:30:04) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
from PIL import Image
import os

def convert_to_bin(data):
    """Convert data to binary format as string"""
    return ''.join(format(ord(i), '08b') for i in data)

def modify_pixel(pixel, bit):
    """Modify the least significant bit of a pixel"""
    pixel = list(pixel)
    pixel[-1] = int(pixel[-1] & 254 | int(bit))
    return tuple(pixel)

def hide_data(image_path, secret_message, output_path):
    """Hide data within an image using LSB"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")
    
    secret_message += chr(0)  # Add a null character to mark the end of the message
    binary_message = convert_to_bin(secret_message)
    index = 0

    image = Image.open(image_path)
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        if index < len(binary_message):
            new_pixel = modify_pixel(pixel, binary_message[index])
            new_pixels.append(new_pixel)
            index += 1
        else:
            new_pixels.append(pixel)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_path)
    print(f"Message hidden successfully in {output_path}")

def extract_data(image_path):
    """Extract data from an image using LSB"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file {image_path} does not exist.")
    
    image = Image.open(image_path)
    pixels = list(image.getdata())
    binary_message = ''

    for pixel in pixels:
        binary_message += str(pixel[-1] & 1)

    binary_message = binary_message.split('00000000')[0]  # Split at null character
...     secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
...     return secret_message
... 
... def main():
...     print("Welcome to Steganography Tool")
...     print("1. Hide a message in an image")
...     print("2. Extract a message from an image")
...     
...     choice = input("Enter your choice (1 or 2): ")
...     
...     if choice == '1':
...         image_path = input("Enter the path to the image: ")
...         secret_message = input("Enter the secret message: ")
...         output_path = input("Enter the path to save the stego image: ")
...         try:
...             hide_data(image_path, secret_message, output_path)
...         except Exception as e:
...             print(f"Error: {e}")
...     elif choice == '2':
...         image_path = input("Enter the path to the stego image: ")
...         try:
...             secret_message = extract_data(image_path)
...             print(f"Extracted Message: {secret_message}")
...         except Exception as e:
...             print(f"Error: {e}")
...     else:
...         print("Invalid choice. Please enter 1 or 2.")
... 
... if _name_ == "_main_":
