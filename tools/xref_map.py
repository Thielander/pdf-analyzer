from PyPDF2 import PdfReader
import re

def list_objects_and_xref(pdf_path):
    """
    Parses the raw PDF file and lists all indirect object definitions and their byte offsets.
    """
    print("[*] PDF Object Map and XRef Table (estimated by scanning raw content):\n")
    try:
        with open(pdf_path, "rb") as f:
            content = f.read().decode("latin1", errors="ignore")

        matches = list(re.finditer(r"(\d+)\s+(\d+)\s+obj", content))
        if not matches:
            print("[!] No indirect objects found.")
            return

        seen_ids = {}
        duplicates = []

        for match in matches:
            obj_num = int(match.group(1))
            gen_num = int(match.group(2))
            offset = match.start()
            key = f"{obj_num} {gen_num}"
            if key in seen_ids:
                duplicates.append(key)
            else:
                seen_ids[key] = offset
            print(f"Object {obj_num:<5} Gen {gen_num:<3} → Offset: {offset}")

        print("\n[*] Duplicate object IDs:")
        if duplicates:
            for dup in duplicates:
                print(f"- {dup}")
        else:
            print("No duplicates found.")

    except Exception as e:
        print(f"[ERROR] Failed to read PDF content: {str(e)}")
