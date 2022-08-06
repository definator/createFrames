#! /usr/bin/python
import sys
import random
import os
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

counter = 0
WATERMARKED_DIR_NAME = 'watermarked'
ORIGINAL_DIR_PATH = os.path.abspath('.')
WATERMARKED_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, WATERMARKED_DIR_NAME)
FONT_DIR_NAME = 'fonts'
FONT_DIR_PATH = os.path.join(ORIGINAL_DIR_PATH, FONT_DIR_NAME)
IMAGE_EXTENSIONS = ('.png', '.webp', '.jpg', '.jpeg')
RESULT_EXTENSION = '.png'

##########################################
##########################################
##########################################
def get_images(dir):
    image_list = os.listdir(ORIGINAL_DIR_PATH)
    filenames = []
    for name in image_list:
        file_extension = os.path.splitext(name)[1]
        if(file_extension in IMAGE_EXTENSIONS):
            filenames.append(name)
    return filenames


def calculate_howmuch(biggest_side, diff):
    if(diff > 162):
        return (biggest_side, biggest_side)
    else:
        side = biggest_side+int(biggest_side/4)
        return (side, side)

def create_aside_frame(width, height):
    if(width > height):
        return (width, (height + int(width / 4)))
    else:
        return ((width + int(height / 4)), height)


def create_around_frame(width, height):
    frame_width = height + int(width / 4)
    frame_height = width + int(height / 4)
    return (frame_width, frame_height)

def watermark(imagepath):
    print('watermark '+imagepath)
    original_image = Image.open(imagepath)
    around_chance = random.randint(1, 100)
    orim_width = original_image.width
    orim_height = original_image.height
    if(around_chance > 75):
        size_of_under_image = create_around_frame(orim_width, orim_height)
    else:
        size_of_under_image = create_aside_frame(orim_width, orim_height)
    # if(orim_height > orim_width):
    #     diff = orim_height - orim_width
    #     size_of_under_image = calculate_howmuch(orim_height, diff)

    # elif(orim_width > orim_height):
    #     diff = orim_width - orim_height
    #     size_of_under_image = calculate_howmuch(orim_width, diff)
    bg_color_chance = random.randint(1, 100)
    if(bg_color_chance > 30):
        bg_color = "white"
    else:
        bg_color = "black"
    frame_image = Image.new('RGB', size_of_under_image, color = bg_color)
    width, height = frame_image.size
    offset = (int((width - orim_width) / 2), int((height - orim_height) / 2))
    frame_image.paste(original_image, offset)
    return frame_image
    
def make_directory():
    isExist = os.path.exists(WATERMARKED_DIR_PATH)
    if not isExist:
        os.makedirs(WATERMARKED_DIR_PATH)
def watermark_all_originals():
    original_image_names = get_images(ORIGINAL_DIR_PATH)
    for imagename in original_image_names:
        global counter
        counter = counter+1
        imagepath = os.path.join(ORIGINAL_DIR_PATH, imagename)
        frame_image = watermark(imagepath)
        # metadata = get_exif(imagename)
        new_file_name = str(counter)+'.png'
        save_file_path = os.path.join(WATERMARKED_DIR_PATH, new_file_name)
        make_directory()
        frame_image.save(save_file_path)
        print(counter)

def rewatermark(filenames):
    for filename in filenames:
        full_filename = filename + RESULT_EXTENSION
        path_to_old_wm_image = os.path.join(WATERMARKED_DIR_PATH, full_filename)
        old_wm_image = Image.open(path_to_old_wm_image)
        print(path_to_old_wm_image)
        metadata = old_wm_image.text
        original_name = metadata['originalName']
        new_meta = get_exif(original_name)
        path_to_original = os.path.join(ORIGINAL_DIR_PATH, original_name)
        watermarked_image = watermark(path_to_original)
        watermarked_image.show()
        watermarked_image.save(path_to_old_wm_image, pnginfo=new_meta)



args = sys.argv
if(len(args) > 1):
    filenames = args[1:]
    rewatermark(filenames)
else:
    watermark_all_originals()
