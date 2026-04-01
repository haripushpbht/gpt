import io
import re
from typing import BinaryIO

from PIL import Image, ImageOps
import pytesseract


def clean_extracted_text(text: str) -> str:
    """Normalize OCR text by removing noisy symbols and extra spaces."""
    text = text.replace("\r", "\n")
    text = re.sub(r"[^\w\s\n\+\-\*/=\^\(\)\[\]\{\}\.\,:%]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def extract_text_from_image(file_like: BinaryIO | io.BytesIO) -> str:
    """Read image stream and run OCR with basic preprocessing."""
    image = Image.open(file_like)
    gray = ImageOps.grayscale(image)
    enhanced = ImageOps.autocontrast(gray)

    raw_text = pytesseract.image_to_string(enhanced, config="--oem 3 --psm 6")
    cleaned = clean_extracted_text(raw_text)

    if not cleaned:
        raise ValueError("Unable to detect readable text from image.")

    return cleaned
