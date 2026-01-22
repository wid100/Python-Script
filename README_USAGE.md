# PDF to CSV - Complete Processing

## Quick Start

### Windows:
```bash
run.bat
```

### বা Python দিয়ে:
```bash
python process_pdf_complete.py
```

## কি করবে:

1. **PDF থেকে CSV** - PDF file খুঁজে CSV-তে convert করবে
2. **Encoding Fix** - Replacement characters () fix করবে
3. **Data Structure** - প্রতিটি মানুষের জন্য আলাদা row তৈরি করবে
4. **ই-কার Fix** - সব ই-কার encoding issues fix করবে
5. **Final CSV** - Clean, structured CSV file তৈরি করবে

## Output Files:

1. `[filename].csv` - Raw CSV from PDF
2. `[filename]_structured.csv` - Structured data (one person per row)
3. `[filename]_structured_final.csv` - **Final clean file (এইটা ব্যবহার করুন)**

## Final File Structure:

- **Name** - নাম
- **NID** - ভোটার নং
- **Father** - পিতা
- **Mother** - মাতা
- **DOB** - জন্মতারিখ
- **Profession** - পেশা
- **Address** - ঠিকানা
- **Page** - পৃষ্ঠা নম্বর

## Example:

```bash
# Just run this:
python process_pdf_complete.py

# Output:
# [FINAL] Output file: filename_structured_final.csv
```

## Note:

- PDF file same directory-তে থাকতে হবে
- সব processing automatically হবে
- Final file ready to use!
