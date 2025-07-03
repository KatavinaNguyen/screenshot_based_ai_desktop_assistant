"""
this should return text in the terminal for the eclip_ss.png that's in the actual folder
"""


from capture.text_extract import extract_text_from_image

image_path = "../capture/img/eclip_ss.png"
text = extract_text_from_image(image_path)
print("Extracted OCR Text:\n", text)
