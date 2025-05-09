# tools/encryptor.py (erweitert)

from PyPDF2 import PdfReader, PdfWriter

def encrypt_pdf(input_path, output_path, password):
    """
    Encrypts a PDF file with a user-supplied password.
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"[+] PDF successfully encrypted and saved as '{output_path}'.")

    except Exception as e:
        print(f"[ERROR] Failed to encrypt PDF: {str(e)}")

def decrypt_pdf(input_path, output_path, password):
    """
    Decrypts a password-protected PDF file using the provided password.
    """
    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            if not reader.decrypt(password):
                print("[ERROR] Incorrect password or decryption failed.")
                return

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"[+] PDF successfully decrypted and saved as '{output_path}'.")

    except Exception as e:
        print(f"[ERROR] Failed to decrypt PDF: {str(e)}")
