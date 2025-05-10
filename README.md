# PDF Analyzer (BETA) 🕵️‍♂️

A powerful, modular PDF analysis toolkit written in Python — inspired by tools like **PDF Stream Dumper**, **pdf-parser**, **ExifTool**, and **PDF CanOpener**. Includes integrated GPT-4 analysis for deeper inspection of embedded content.

---

## 📦 Features

- Extract **URLs**, **IP addresses**, and **text**
- Detect **embedded JavaScript**
- Show **PDF metadata**
- Generate **file hashes** (MD5, SHA1, SHA256)
- Perform **AI analysis using OpenAI GPT**
- Output detailed **PDF reports**

---

## 🛠 Installation

- git clone https://github.com/thielander/pdf-analyzer.git
- cd pdf-analyzer
- python3 -m venv venv
- source venv/bin/activate  # Windows: venv\Scripts\activate
- pip install -r requirements.txt
- mv .env.example .env

---

## 🚀 Usage

python main.py path/to/file.pdf [options]

### Available Options

** Option	Description **
- -h, --help            show this help message and exit
- -e, --extract         Extract URLs and IPs from the document
- -js, --javascript     Analyze the document for JavaScript code
- -m, --metadata        Display PDF metadata
- -t, --text            Extract visible text from the PDF
- --hash                Generate file hashes (MD5, SHA1, SHA256)
- --gpt-analyze         Analyze document content using OpenAI GPT and generate PDF report
- --view-code           Show raw PDF code as text
- --search TERM         Highlight specific term in PDF code view
- --xref-map            List all PDF objects and their xref positions
- --embedded            List embedded files in the PDF
- --suspicious-actions  Scan for suspicious PDF actions like /Launch, /URI, /SubmitForm
- --entropy             Analyze entropy of all PDF stream objects
- --dump-streams        Dump all decompressed stream contents
- --deobfuscate         Detect and decode obfuscated JavaScript from PDF content
- --encrypt PWD         Encrypt PDF with the specified password
- --out OUTPUT          Specify output filename for encrypted PDF
- --decrypt PWD         Decrypt a password-protected PDF
- --bruteforce WORDLIST
                        Try to brute-force the PDF password using a wordlist file
(venv) alexanderthiele@Mac pdf-analyzer % 

---

## 📄 Example

- python main.py samples/malicious.pdf -e -js --gpt-analyze
