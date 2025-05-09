# PDF Analyzer 🕵️‍♂️

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

git clone https://github.com/thielander/pdf-analyzer.git
cd pdf-analyzer
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
mv .env.example .env

---

## 🚀 Usage

python main.py path/to/file.pdf [options]

### Available Options

Option	Description
-e	Extract URLs and IPs
-js	Detect embedded JavaScript
-m	Show metadata
-t	Extract visible text
--hash	Generate MD5/SHA1/SHA256 hashes
--gpt-analyze	Analyze content with OpenAI GPT-4 and save PDF

---

## 📄 Example

python main.py samples/malicious.pdf -e -js --gpt-analyze
