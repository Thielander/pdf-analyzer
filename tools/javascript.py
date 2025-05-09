# javascript.py

from PyPDF2 import PdfReader

def extract_javascript(pdf_path):
    reader = PdfReader(pdf_path)
    js_scripts = []

    for page in reader.pages:
        try:
            if "/AA" in page:
                aa = page["/AA"]
                if "/JS" in aa:
                    js_scripts.append(aa["/JS"])
        except Exception:
            continue

    if "/Names" in reader.trailer["/Root"]:
        names = reader.trailer["/Root"]["/Names"]
        if "/JavaScript" in names:
            js_names = names["/JavaScript"]["/Names"]
            for i in range(1, len(js_names), 2):
                js_scripts.append(js_names[i].get_object())

    return js_scripts
