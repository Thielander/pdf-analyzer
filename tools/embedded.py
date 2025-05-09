from PyPDF2 import PdfReader

def list_embedded_files(pdf_path):
    """
    Detects and lists embedded files in a PDF document.
    Resolves indirect objects correctly and shows name, size, and subtype.
    """
    try:
        reader = PdfReader(pdf_path)
        catalog = reader.trailer["/Root"]

        names_obj = catalog.get("/Names")
        if not names_obj:
            print("[+] No embedded files found (no /Names dictionary).")
            return

        names = names_obj.get_object()
        embedded_files_obj = names.get("/EmbeddedFiles")
        if not embedded_files_obj:
            print("[+] No embedded files found (no /EmbeddedFiles entry).")
            return

        embedded_files = embedded_files_obj.get_object()
        files = embedded_files.get("/Names")
        if not files or len(files) == 0:
            print("[+] No embedded files found (empty /EmbeddedFiles list).")
            return

        print("[*] Embedded Files Found:\n")

        for i in range(0, len(files), 2):
            name = files[i]
            file_spec = files[i + 1].get_object()

            ef_dict = file_spec.get("/EF")
            if ef_dict and "/F" in ef_dict:
                file_stream = ef_dict["/F"].get_object()
                size = file_stream.get("/Length", "Unknown")
                subtype = file_stream.get("/Subtype", "N/A")

                print(f"File Name : {name}")
                print(f"Size      : {size} bytes")
                print(f"Subtype   : {subtype}")
                print("-" * 40)
            else:
                print(f"[!] Embedded file '{name}' has no /F stream.")
    except Exception as e:
        print(f"[ERROR] Failed to scan for embedded files: {str(e)}")
