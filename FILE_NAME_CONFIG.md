# File Name Configuration Guide

## PDF File Naming:
আপনার PDF file-গুলো number দিয়ে রাখুন:
- `001.pdf`
- `002.pdf`
- `003.pdf`
- ইত্যাদি

## CSV Output Files:
Script automatically same name দিয়ে CSV তৈরি করবে:
- `001.pdf` → `001.csv`, `001_structured.csv`, `001_structured_final.csv`
- `002.pdf` → `002.csv`, `002_structured.csv`, `002_structured_final.csv`

## Usage:

### Method 1: Command line argument
```bash
python process_pdf_complete.py 001.pdf
python process_pdf_complete.py 002.pdf
```

### Method 2: Batch file (Windows)
```bash
run_with_pdf.bat
```
তারপর PDF file name দিন (e.g., 001.pdf)

### Method 3: Auto-detect (first PDF in folder)
```bash
python process_pdf_complete.py
```

## কোথায় কোথায় File Name Change করতে হবে:

### 1. Script Run করার সময়:
```bash
python process_pdf_complete.py 001.pdf
```
এখানে `001.pdf` change করুন আপনার PDF file name দিয়ে।

### 2. Batch File ব্যবহার করলে:
`run_with_pdf.bat` run করুন, তারপর prompt এ file name দিন।

### 3. Script-এ Hardcode করতে চাইলে:
`process_pdf_complete.py` file-এ line 38-42 এ:
```python
pdf_filename = "001.pdf"  # এখানে আপনার file name দিন
pdf_file = Path(pdf_filename)
```

## Output File Names:
Script automatically same base name use করবে:
- Input: `001.pdf`
- Output: 
  - `001.csv` (raw)
  - `001_structured.csv` (structured)
  - `001_structured_final.csv` (final - এইটা use করুন)

## Example:
```bash
# For 001.pdf
python process_pdf_complete.py 001.pdf
# Output: 001_structured_final.csv

# For 002.pdf  
python process_pdf_complete.py 002.pdf
# Output: 002_structured_final.csv
```
