# Re-defining code after state reset

# extractor.py

import re
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_metadata(pdf_path):
    reader = PdfReader(pdf_path)
    return reader.metadata

def extract_urls_and_ips(text):
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    urls = re.findall(url_pattern, text)
    ips = re.findall(ip_pattern, text)
    return urls, ips
