# tools/bruteforce.py

from PyPDF2 import PdfReader

def bruteforce_pdf_password(pdf_path, wordlist_path):
    """
    Attempts to decrypt a PDF using a list of passwords from a wordlist file.
    """
    try:
        with open(wordlist_path, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] Failed to read wordlist: {str(e)}")
        return

    try:
        reader = PdfReader(pdf_path)
        if not reader.is_encrypted:
            print("[+] PDF is not encrypted.")
            return

        print(f"[*] Starting brute-force with {len(passwords)} passwords...\n")

        for pw in passwords:
            try:
                if reader.decrypt(pw):
                    print(f"[+] Password found: '{pw}'")
                    return
            except Exception:
                continue

        print("[-] No valid password found.")
    except Exception as e:
        print(f"[ERROR] Brute-force failed: {str(e)}")
