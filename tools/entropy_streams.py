# tools/entropy_streams.py

import math
from PyPDF2 import PdfReader
import zlib

def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of a byte string."""
    if not data:
        return 0.0
    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1
    entropy = 0.0
    for count in byte_counts:
        if count == 0:
            continue
        p = count / len(data)
        entropy -= p * math.log2(p)
    return entropy

def analyze_entropy(pdf_path):
    """Scan all stream objects and calculate entropy."""
    try:
        reader = PdfReader(pdf_path)
        print("[*] Stream Entropy Analysis:\n")
        index = 0
        for page in reader.pages:
            if "/Contents" in page:
                contents = page["/Contents"]
                if not isinstance(contents, list):
                    contents = [contents]
                for content in contents:
                    try:
                        stream = content.get_object()
                        data = stream.get_data()
                        entropy = calculate_entropy(data)
                        print(f"Object #{index} - Entropy: {entropy:.4f} - Length: {len(data)} bytes")
                    except Exception:
                        continue
            index += 1
    except Exception as e:
        print(f"[ERROR] Failed entropy analysis: {str(e)}")

def dump_all_streams(pdf_path):
    """Dump and decompress all stream objects."""
    try:
        reader = PdfReader(pdf_path)
        print("[*] Dumping all decompressed stream contents:\n")
        for i, page in enumerate(reader.pages):
            if "/Contents" in page:
                contents = page["/Contents"]
                if not isinstance(contents, list):
                    contents = [contents]
                for j, content in enumerate(contents):
                    try:
                        stream = content.get_object()
                        data = stream.get_data()
                        print(f"\n[Stream Page {i+1} - Block {j+1} | Length: {len(data)} bytes]")
                        print(data.decode('latin1', errors='ignore'))
                    except Exception as e:
                        print(f"[!] Failed to decompress stream on page {i+1}: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Failed stream dump: {str(e)}")

