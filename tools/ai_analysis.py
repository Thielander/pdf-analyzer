from dotenv import load_dotenv
import os
import fitz
from openai import OpenAI
from tools.raw_structure import extract_raw_structure

# Load API config from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4")
system_prompt = os.getenv("OPENAI_SYSTEM_PROMPT")
temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))

client = OpenAI(api_key=api_key)

def extract_text_for_ai(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text  # Full visible content

def analyze_with_openai(content):
    if not api_key:
        return "[Error] OPENAI_API_KEY not set. Please check your .env file."
    if not system_prompt:
        return "[Error] OPENAI_SYSTEM_PROMPT not set. Please define it in .env."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{content}"}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error communicating with OpenAI API] {str(e)}"

def run_openai_analysis(pdf_path):
    visible_text = extract_text_for_ai(pdf_path)

    structure = extract_raw_structure(pdf_path)
    structure_text = f"""
PDF Header:
{structure['header']}

XRef Table:
{structure['xref']}

Trailer:
{structure['trailer']}

First 10 Objects:
"""
    for i, obj in enumerate(structure['objects'][:5], 1):  # optional Begrenzung
        structure_text += f"\n[Object {i}]\n{obj.strip()}\n"

    combined_input = (
        "=== Visible Content ===\n" + visible_text +
        "\n\n=== Raw Structure ===\n" + structure_text
    )

    return analyze_with_openai(combined_input)

