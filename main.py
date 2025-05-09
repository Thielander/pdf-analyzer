# main.py

import argparse
import os
import platform
from tools.extractor import extract_text, extract_metadata, extract_urls_and_ips
from tools.javascript import extract_javascript
from tools.hasher import hash_file
from tools.ai_analysis import run_openai_analysis
from tools.codeviewer import view_pdf_code


VERSION = "1.0"

def print_banner():
    print(rf"""
        \|||/
        (o o)
,~~~ooO~~(_)~~~~~~~~~,
|  Alexander Thiele  |
|    PDF Analyzer    |
|     Version {VERSION}    |
'~~~~~~~~~~~~~~ooO~~~'
       |__|__|
        || ||
       ooO Ooo
""")


def clear_screen():
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)

def main():
    clear_screen()
    print_banner()
    parser = argparse.ArgumentParser(
        description="PDF Analyzer - A modular PDF analysis toolkit with GPT support."
    )
    parser.add_argument("file", nargs="?", help="Path to the PDF file")
    parser.add_argument("-e", "--extract", action="store_true", help="Extract URLs and IPs from the document")
    parser.add_argument("-js", "--javascript", action="store_true", help="Analyze the document for JavaScript code")
    parser.add_argument("-m", "--metadata", action="store_true", help="Display PDF metadata")
    parser.add_argument("-t", "--text", action="store_true", help="Extract visible text from the PDF")
    parser.add_argument("--hash", action="store_true", help="Generate file hashes (MD5, SHA1, SHA256)")
    parser.add_argument("--view-code", action="store_true", help="Show raw PDF code as text")
    parser.add_argument("--gpt-analyze", action="store_true", help="Analyze document content using OpenAI GPT and generate PDF report")

    args = parser.parse_args()

    if not args.file:
        print("[!] No PDF file specified.\n")
        parser.print_help()
        return


    file_path = args.file

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    if args.view_code:
        print("[*] Showing raw PDF code...\n")
        view_pdf_code(file_path)


    if args.extract:
        print("[*] Extracting URLs and IP addresses...")
        text = extract_text(file_path)
        urls, ips = extract_urls_and_ips(text)
        print("\n[+] URLs:")
        for url in urls:
            print(" -", url)
        print("\n[+] IP Addresses:")
        for ip in ips:
            print(" -", ip)
            print()
             
    if args.javascript:
        print("[*] Scanning for embedded JavaScript...")
        scripts = extract_javascript(file_path)
        if scripts:
            print(f"[+] Found {len(scripts)} JavaScript blocks:")
            for i, script in enumerate(scripts, start=1):
                print(f"\n[Script #{i}]:\n{script}")
        else:
            print("[+] No JavaScript found.")

    if args.metadata:
        print("[*] Reading metadata...")
        metadata = extract_metadata(file_path)
        if metadata:
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print("[+] No metadata available.")

    if args.text:
        print("[*] Extracting visible text from PDF...")
        text = extract_text(file_path)
        print(text)


    if args.hash:
        print("[*] Calculating file hashes...")
        hashes = hash_file(file_path)
        for algo, value in hashes.items():
            print(f"{algo.upper()}: {value}")

    if args.gpt_analyze:
        print()  # Leerzeile für optische Trennung
        print("[*] Running GPT analysis...")
        result = run_openai_analysis(file_path)
        print("\n[+] GPT Analysis Output:\n")
        print("=" * 60)
        print(result)
        print("=" * 60)



if __name__ == "__main__":
    main()
