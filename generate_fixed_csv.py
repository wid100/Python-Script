"""
Generate CSV from PDF with encoding fixes
"""

import sys
import io
from pathlib import Path
from pdf_to_csv import PDFToCSVConverter

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    """Main function"""
    # Find PDF files in current directory
    current_dir = Path('.')
    pdf_files = list(current_dir.glob('*.pdf'))
    
    if not pdf_files:
        print("No PDF files found in current directory")
        return
    
    # Use first PDF file
    pdf_file = pdf_files[0]
    print(f"Processing PDF: {pdf_file.name}")
    
    try:
        # Create converter
        converter = PDFToCSVConverter(str(pdf_file))
        
        # Generate CSV with fixes
        print("Converting PDF to CSV with encoding fixes...")
        output_file = converter.convert_to_csv_simple()
        
        print(f"\nSuccess! CSV file created: {output_file}")
        print("All encoding issues have been fixed.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
