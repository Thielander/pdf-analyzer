from PyPDF2 import PdfReader

SUSPICIOUS_KEYS = ["/Launch", "/URI", "/GoTo", "/SubmitForm", "/Named", "/OpenAction", "/AA"]

def scan_suspicious_actions(pdf_path):
    """
    Scans for suspicious or auto-executing actions like /Launch, /URI, etc.
    Uses recursion guard to avoid infinite loops.
    """
    try:
        reader = PdfReader(pdf_path)
        found = []
        seen = set()

        def check_dict(obj, path=""):
            if not isinstance(obj, dict):
                return

            obj_id = id(obj)
            if obj_id in seen:
                return
            seen.add(obj_id)

            for key, value in obj.items():
                if key in SUSPICIOUS_KEYS:
                    found.append((path + key, str(value)))

                # check substructure
                if isinstance(value, dict):
                    check_dict(value, path + key + "->")
                elif hasattr(value, "get_object"):
                    try:
                        sub = value.get_object()
                        if isinstance(sub, dict):
                            check_dict(sub, path + key + "->")
                    except Exception:
                        continue

        check_dict(reader.trailer)

        if found:
            print("[*] Suspicious PDF actions detected:\n")
            for key_path, val in found:
                print(f"{key_path}: {val}")
        else:
            print("[+] No suspicious actions found.")

    except Exception as e:
        print(f"[ERROR] Failed to scan for suspicious actions: {str(e)}")
