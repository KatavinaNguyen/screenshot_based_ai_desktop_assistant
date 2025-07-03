"""
Uses PaddleOCR to extract and return text from an image (user's screenshot, returns to snip_tool.py).
"""
from paddleocr import PaddleOCR
import logging

logging.getLogger("ppocr").setLevel(logging.ERROR)  # Suppress noisy PaddleOCR logs
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # Initialize OCR instance

def extract_text_from_image(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    result = ocr.ocr(image_path, cls=True)

    extracted_text_list = []
    for line in result[0]:
        text = line[1][0]
        extracted_text_list.append(text)

    return "\n".join(extracted_text_list)
