# tools/deobfuscator.py

import re
import base64
import binascii
from PyPDF2 import PdfReader

def deobfuscate_pdf_javascript(pdf_path):
    """
    Searches for JavaScript in the text and tries to deobfuscate typical encodings:
    - Base64
    - Hex
    - Unicode escapes
    """
    try:
        reader = PdfReader(pdf_path)
        print("[*] Scanning for obfuscated JavaScript and decoding it...\n")

        found = False

        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            # Base64 pattern
            base64_matches = re.findall(r"[A-Za-z0-9+/=]{20,}", text)
            for match in base64_matches:
                try:
                    decoded = base64.b64decode(match).decode("utf-8", errors="ignore")
                    if "function" in decoded or "eval" in decoded:
                        print(f"[Base64 Page {i}]")
                        print(decoded)
                        found = True
                except Exception:
                    continue

            # Hex pattern: e.g. \x61\x62...
            hex_matches = re.findall(r"(?:\\x[0-9a-fA-F]{2}){4,}", text)
            for match in hex_matches:
                try:
                    bytestr = bytes([int(h[2:], 16) for h in re.findall(r"\\x[0-9a-fA-F]{2}", match)])
                    decoded = bytestr.decode("utf-8", errors="ignore")
                    print(f"[Hex Page {i}]")
                    print(decoded)
                    found = True
                except Exception:
                    continue

            # Unicode escapes: \u0061\u0062...
            uni_matches = re.findall(r"(?:\\u[0-9a-fA-F]{4}){2,}", text)
            for match in uni_matches:
                try:
                    decoded = bytes(match, "utf-8").decode("unicode_escape")
                    print(f"[Unicode Page {i}]")
                    print(decoded)
                    found = True
                except Exception:
                    continue

        if not found:
            print("[+] No obfuscated JavaScript found.")
    except Exception as e:
        print(f"[ERROR] Deobfuscation failed: {str(e)}")
