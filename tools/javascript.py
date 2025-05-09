from PyPDF2 import PdfReader

def extract_javascript(pdf_path):
    reader = PdfReader(pdf_path)
    js_scripts = []

    # Check for /Names -> /JavaScript
    try:
        names = reader.trailer["/Root"].get("/Names", {})
        if "/JavaScript" in names:
            js_entries = names["/JavaScript"]["/Names"]
            for i in range(1, len(js_entries), 2):
                js_obj = js_entries[i].get_object()
                js_code = js_obj.get("/JS")
                if js_code:
                    js_scripts.append(js_code)
    except Exception:
        pass

    # Check for /OpenAction JavaScript
    try:
        open_action = reader.trailer["/Root"].get("/OpenAction", {})
        if "/JS" in open_action:
            js_scripts.append(open_action["/JS"])
    except Exception:
        pass

    # Check all pages for /AA -> /JS (Additional Actions)
    for page in reader.pages:
        try:
            aa = page.get("/AA", {})
            for key in aa:
                action = aa[key]
                js = action.get("/JS")
                if js:
                    js_scripts.append(js)
        except Exception:
            continue

    # Search for /AcroForm -> /Fields with JS
    try:
        acro_form = reader.trailer["/Root"].get("/AcroForm", {})
        fields = acro_form.get("/Fields", [])
        for field in fields:
            field_obj = field.get_object()
            additional_actions = field_obj.get("/AA", {})
            for action_key in additional_actions:
                action = additional_actions[action_key]
                js = action.get("/JS")
                if js:
                    js_scripts.append(js)
    except Exception:
        pass

    return js_scripts
