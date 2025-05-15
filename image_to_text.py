# image recognition, image output text from image
# depends, pip install pytesseract pillow opencv-python
# other depends, tesseractOCR installed (https://github.com/tesseract-ocr/tesseract/releases)
# use config.ini for tesseract exe path and image
# image can be overridden with --image imagefile

import cv2
import pytesseract
from PIL import Image
import configparser
import argparse
import os

# create default ini file as text (config.ini)
DEFAULT_CONFIG="""\
[Tesseract]
cmd_path = C:\\Program Files\\Tesseract-OCR\\tesseract.exe
args = --psm 6

[Input]
image_file = sample.jpg
"""

# check/create ini file
def ensure_config_exists(config_file="config.ini"):
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write(DEFAULT_CONFIG)
        print(f"created default: {config_file}")

ensure_config_exists()

parser=argparse.ArgumentParser()
parser.add_argument("--image", type=str, help="override image file path")
args=parser.parse_args()

config=configparser.ConfigParser()
config.read("config.ini")

pytesseract.pytesseract.tesseract_cmd=config["Tesseract"]["cmd_path"]
image_file=config["Input"]["image_file"]
tesseract_args=config["Tesseract"]["args"]

#apply settings
pytesseract.pytesseract.tesseract_cmd=config["Tesseract"]["cmd_path"]
image_file=config["Input"]["image_file"]
tesseract_args=config["Tesseract"]["args"]

# ovveride image if necessary
if args.image:
    image_file=args.image

def extract_text(image_path):
    image=cv2.imread(image_path)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    processed_image=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # ocr text extract
    text = pytesseract.image_to_string(processed_image)
    return text
    
#extract to text
text=extract_text(image_file)
print(text)