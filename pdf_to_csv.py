"""
PDF to CSV Converter for Bengali Text
Handles Bijoy keyboard layout and converts PDF data to CSV format
"""

import pdfplumber
import pandas as pd
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional


class PDFToCSVConverter:
    """Convert PDF files containing Bengali text to CSV format"""
    
    def __init__(self, pdf_path: str):
        """
        Initialize the converter with PDF file path
        
        Args:
            pdf_path: Path to the input PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    def extract_text_from_pdf(self) -> List[Dict]:
        """
        Extract text from PDF pages
        
        Returns:
            List of dictionaries containing page number and extracted text
        """
        extracted_data = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                print(f"Total pages: {len(pdf.pages)}")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    print(f"Processing page {page_num}...")
                    
                    # Extract text with layout preservation
                    text = page.extract_text()
                    
                    # Try to extract tables if available
                    tables = page.extract_tables()
                    
                    if tables:
                        # If tables are found, use table data
                        for table_idx, table in enumerate(tables):
                            if table:
                                # Clean table data
                                cleaned_table = self._clean_table_data(table)
                                extracted_data.append({
                                    'page': page_num,
                                    'table_index': table_idx,
                                    'type': 'table',
                                    'data': cleaned_table
                                })
                    
                    if text:
                        # Clean and process text
                        cleaned_text = self._clean_bengali_text(text)
                        extracted_data.append({
                            'page': page_num,
                            'type': 'text',
                            'data': cleaned_text
                        })
        
        except Exception as e:
            print(f"Error extracting PDF: {str(e)}")
            raise
        
        return extracted_data
    
    def _clean_bengali_text(self, text: str) -> str:
        """
        Clean and fix Bengali text, especially for Bijoy keyboard issues
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned Bengali text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common Bijoy keyboard encoding issues
        # You may need to add more mappings based on your specific issues
        text = self._fix_bijoy_encoding(text)
        
        # Remove non-printable characters but keep Bengali Unicode
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def _fix_bijoy_encoding(self, text: str) -> str:
        """
        Fix common Bijoy keyboard encoding issues and replacement characters
        
        Args:
            text: Text with potential encoding issues
            
        Returns:
            Fixed text
        """
        if not text:
            return text
        
        # First fix specific known patterns with replacement character
        specific_fixes = [
            ('ভাটার', 'ভোটার'),
            ('কাড', 'কোড'),
            ('রাড', 'রোড'),
            ('মাহাম্মদ', 'মোহাম্মদ'),
            ('মাসােদ্দক', 'মোসাদ্দেক'),
            ('মাসাম্মৎ', 'মোসাম্মৎ'),
            ('মাসাম্মত', 'মোসাম্মত'),
            ('মাসিলম', 'মোছলিম'),
            ('মাহাঃ', 'মোহাঃ'),
            ('মাসাঃ', 'মোসাঃ'),
            ('মাছাঃ', 'মোছাঃ'),
            ('মাঃ', 'মোঃ'),
            ('বগম', 'বেগম'),
            ('পশা', 'পেশা'),
            ('কন্দ্র', 'কেন্দ্র'),
            ('সয়দা', 'সয়দা'),
            ('সয়দ', 'সয়দ'),
            ('খােদজা', 'খোদেজা'),
            ('জােবদা', 'জোবেদা'),
            ('নওয়াজ', 'নওয়াজ'),
            ('গালাম', 'গোলাম'),
            ('ফরেদৌসী', 'ফরিদৌসী'),
            ('শখ', 'শেখ'),
            ('রজওয়ানা', 'রেজওয়ানা'),
            ('রজাউল', 'রেজাউল'),
            ('হােসন', 'হোসেন'),
            ('কায়াটার', 'কোয়ার্টার'),
            ('কায়াটা', 'কোয়ার্টার'),
            ('কায়াট', 'কোয়ার্টার'),
            ('গালস', 'গার্লস'),
            ('টচার', 'টিচার'),
        ]
        
        # Apply specific fixes
        for old, new in specific_fixes:
            text = text.replace(old, new)
        
        # Remove replacement character () - it's Unicode U+FFFD
        # This character appears when encoding fails
        text = text.replace('\ufffd', '')
        text = text.replace('', '')  # Also try empty string replacement
        
        # Common Bijoy to Unicode mappings
        bijoy_fixes = {
            # Add specific character mappings here if needed
            # Example: 'à¦' : 'া', etc.
        }
        
        for old_char, new_char in bijoy_fixes.items():
            text = text.replace(old_char, new_char)
        
        return text
    
    def _clean_table_data(self, table: List[List]) -> List[List]:
        """
        Clean table data and handle Bengali text
        
        Args:
            table: Raw table data from PDF
            
        Returns:
            Cleaned table data
        """
        cleaned_table = []
        
        for row in table:
            if row:
                cleaned_row = []
                for cell in row:
                    if cell:
                        cleaned_cell = self._clean_bengali_text(str(cell))
                        cleaned_row.append(cleaned_cell)
                    else:
                        cleaned_row.append("")
                cleaned_table.append(cleaned_row)
        
        return cleaned_table
    
    def convert_to_csv(self, output_path: Optional[str] = None, 
                      extract_tables: bool = True) -> str:
        """
        Convert PDF to CSV file
        
        Args:
            output_path: Path for output CSV file (optional)
            extract_tables: Whether to extract tables separately
            
        Returns:
            Path to created CSV file
        """
        if output_path is None:
            output_path = self.pdf_path.with_suffix('.csv')
        else:
            output_path = Path(output_path)
        
        # Extract data from PDF
        extracted_data = self.extract_text_from_pdf()
        
        if not extracted_data:
            raise ValueError("No data extracted from PDF")
        
        # Process and convert to DataFrame
        all_rows = []
        
        for item in extracted_data:
            if item['type'] == 'table' and extract_tables:
                # Add table data
                table_data = item['data']
                if table_data:
                    # Use first row as header if available
                    if len(table_data) > 0:
                        for row_idx, row in enumerate(table_data):
                            row_dict = {
                                'Page': item['page'],
                                'Table_Index': item['table_index'],
                                'Row_Index': row_idx
                            }
                            
                            # Add columns dynamically
                            for col_idx, cell_value in enumerate(row):
                                col_name = f'Column_{col_idx + 1}'
                                row_dict[col_name] = cell_value
                            
                            all_rows.append(row_dict)
            
            elif item['type'] == 'text':
                # Add text data
                text_lines = item['data'].split('\n')
                for line_idx, line in enumerate(text_lines):
                    if line.strip():
                        all_rows.append({
                            'Page': item['page'],
                            'Type': 'Text',
                            'Line_Index': line_idx,
                            'Content': line.strip()
                        })
        
        # Create DataFrame and save to CSV
        if all_rows:
            df = pd.DataFrame(all_rows)
            
            # Save with UTF-8 encoding to support Bengali
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"\nCSV file created successfully: {output_path}")
            print(f"Total rows: {len(df)}")
            
            return str(output_path)
        else:
            raise ValueError("No data to write to CSV")
    
    def convert_to_csv_simple(self, output_path: Optional[str] = None) -> str:
        """
        Simple conversion: Extract all text line by line to CSV
        
        Args:
            output_path: Path for output CSV file (optional)
            
        Returns:
            Path to created CSV file
        """
        if output_path is None:
            output_path = self.pdf_path.with_suffix('.csv')
        else:
            output_path = Path(output_path)
        
        all_text_lines = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            cleaned_line = self._clean_bengali_text(line)
                            if cleaned_line.strip():
                                all_text_lines.append({
                                    'Page': page_num,
                                    'Text': cleaned_line
                                })
        
        except Exception as e:
            print(f"Error: {str(e)}")
            raise
        
        if all_text_lines:
            df = pd.DataFrame(all_text_lines)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"\nCSV file created: {output_path}")
            print(f"Total lines: {len(df)}")
            return str(output_path)
        else:
            raise ValueError("No text extracted from PDF")


def main():
    """Main function to run the converter"""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_csv.py <pdf_file_path> [output_csv_path]")
        print("\nExample:")
        print("  python pdf_to_csv.py document.pdf")
        print("  python pdf_to_csv.py document.pdf output.csv")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        converter = PDFToCSVConverter(pdf_path)
        
        # Try simple conversion first
        print("Converting PDF to CSV...")
        converter.convert_to_csv_simple(output_path)
        
        print("\nConversion completed successfully!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
