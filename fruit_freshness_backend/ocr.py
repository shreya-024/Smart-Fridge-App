from paddleocr import PaddleOCR
import re
from datetime import datetime
import cv2
import os

# Initialize PaddleOCR once
ocr = PaddleOCR(use_angle_cls=True, lang='en', det_db_box_thresh=0.3)

def process_image(image_path):
    print(f"[INFO] Processing image: {image_path}")
    result = ocr.ocr(image_path, cls=True)
    text_list = [line[1][0] for block in result for line in block]
    print(f"[OCR] Extracted Text: {' '.join(text_list)}")

    # Add more patterns for compact date formats like 060922 (DDMMYY or MMDDYY)
    for text in text_list:
        # First: try common explicit formats
        patterns = [
            r"(exp.*?[:\s\-]*)(\d{6,8})",
            r"(expiry.*?[:\s\-]*)(\d{6,8})",
            r"(best before.*?[:\s\-]*)(\d{6,8})",
            r"exp(\d{1,2}[a-zA-Z]{3,}[0-9]{4})"  # NEW: matches Exp14APR2024
        ]

        for pattern, fmt in patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group()
                try:
                    expiry = datetime.strptime(date_str, fmt)
                    print(f"[INFO] Expiry Date Detected: {expiry.strftime('%d %b %Y')}")
                    return expiry
                except ValueError:
                    continue

    return None


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    preprocessed_path = "preprocessed.jpg"
    cv2.imwrite(preprocessed_path, thresh)
    return preprocessed_path
