# raw_structure.py

def extract_raw_structure(pdf_path):
    """
    Extract raw PDF structure for forensics:
    - header
    - xref table
    - trailer
    - all obj blocks
    """
    raw_output = {
        "header": "",
        "xref": "",
        "trailer": "",
        "objects": []
    }

    with open(pdf_path, "rb") as f:
        content = f.read()

    text = content.decode("latin1", errors="ignore")

    # Extract header
    if text.startswith("%PDF-"):
        raw_output["header"] = text.splitlines()[0]

    # Extract xref table
    if "xref" in text:
        xref_start = text.find("xref")
        xref_end = text.find("trailer", xref_start)
        raw_output["xref"] = text[xref_start:xref_end].strip()

    # Extract trailer
    if "trailer" in text:
        trailer_start = text.find("trailer")
        startxref = text.find("startxref", trailer_start)
        raw_output["trailer"] = text[trailer_start:startxref].strip()

    # Extract objects
    import re
    object_matches = re.findall(r"\d+ \d+ obj(.*?)endobj", text, re.DOTALL)
    raw_output["objects"] = object_matches[:10]  # Limit for GPT context

    return raw_output
