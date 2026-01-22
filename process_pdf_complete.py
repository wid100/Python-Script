"""
Complete PDF to CSV Processing Pipeline
1. Convert PDF to CSV
2. Fix encoding issues (replacement characters)
3. Structure voter data
4. Fix ই-কার encoding issues
5. Generate final clean CSV

Usage:
    python process_pdf_complete.py [pdf_filename]
    
Example:
    python process_pdf_complete.py 001.pdf
    python process_pdf_complete.py 002.pdf
"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding for output (only if not already set)
if sys.platform == 'win32' and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

def main():
    """Main processing pipeline"""
    print("=" * 60)
    print("PDF to CSV Complete Processing Pipeline")
    print("=" * 60)
    print()
    
    # Step 1: Get PDF file name
    if len(sys.argv) > 1:
        # PDF file name provided as argument
        pdf_filename = sys.argv[1]
        pdf_file = Path(pdf_filename)
        
        if not pdf_file.exists():
            print(f"[ERROR] PDF file not found: {pdf_filename}")
            print("\nUsage: python process_pdf_complete.py [pdf_filename]")
            print("Example: python process_pdf_complete.py 001.pdf")
            return
        
        print(f"Step 1: Using PDF file: {pdf_filename}")
    else:
        # Find PDF file automatically
        print("Step 1: Finding PDF file...")
        current_dir = Path('.')
        pdf_files = list(current_dir.glob('*.pdf'))
        
        if not pdf_files:
            print("[ERROR] No PDF files found in current directory")
            print("\nUsage: python process_pdf_complete.py [pdf_filename]")
            print("Example: python process_pdf_complete.py 001.pdf")
            return
        
        pdf_file = pdf_files[0]
        pdf_filename = pdf_file.name
        print(f"[OK] Found PDF: {pdf_filename}")
    
    print()
    
    # Step 2: Convert PDF to CSV (same name as PDF) - Using Advanced Extractor
    print("Step 2: Converting PDF to CSV (Advanced Extraction)...")
    try:
        import pandas as pd
        
        # Try advanced extractor first (PyMuPDF)
        try:
            from pdf_extractor_advanced import AdvancedPDFExtractor
            print("  Using PyMuPDF for better text extraction...")
            extractor = AdvancedPDFExtractor(str(pdf_file))
            all_text_lines = extractor.extract_text_advanced()
            
            if not all_text_lines or len(all_text_lines) < 10:
                print("  Warning: Limited text extracted, trying fallback method...")
                all_text_lines = extractor.extract_text_with_ocr_fallback()
        
        except ImportError:
            print("  PyMuPDF not available, using pdfplumber...")
            from pdf_to_csv import PDFToCSVConverter
            import pdfplumber
            
            converter = PDFToCSVConverter(str(pdf_file))
            all_text_lines = []
            
            with pdfplumber.open(str(pdf_file)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            cleaned_line = converter._clean_bengali_text(line)
                            if cleaned_line.strip():
                                all_text_lines.append({
                                    'Page': page_num,
                                    'Text': cleaned_line
                                })
        
        # Save to CSV with same name as PDF
        csv_file = pdf_file.with_suffix('.csv')
        if all_text_lines:
            df = pd.DataFrame(all_text_lines)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"[OK] CSV created: {csv_file.name} ({len(df)} lines)")
        else:
            print("[ERROR] No text extracted from PDF")
            return
        print()
    except Exception as e:
        print(f"[ERROR] Error converting PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Fix replacement characters
    print("Step 3: Fixing replacement characters ()...")
    try:
        import pandas as pd
        
        def fix_replacement_characters(text):
            """Remove replacement characters from text"""
            if not text or not isinstance(text, str):
                return text
            # Remove Unicode replacement character (U+FFFD)
            text = text.replace('\ufffd', '')
            text = text.replace('', '')  # Also handle if it appears as empty
            return text
        
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        text_columns = df.select_dtypes(include=['object']).columns
        
        fixed_count = 0
        for col in text_columns:
            before = df[col].astype(str).str.contains('\ufffd', na=False).sum()
            df[col] = df[col].apply(fix_replacement_characters)
            after = df[col].astype(str).str.contains('\ufffd', na=False).sum()
            fixed_count += (before - after)
        
        if fixed_count > 0:
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"[OK] Fixed {fixed_count} replacement characters")
        else:
            print("[OK] No replacement characters found")
        print()
    except Exception as e:
        print(f"[WARNING] Could not fix replacement characters: {str(e)}")
        print()
    
    # Step 4: Structure voter data
    print("Step 4: Structuring voter data into individual rows...")
    try:
        from structure_voter_data_v2 import structure_voter_data
        
        structured_df = structure_voter_data(str(csv_file))
        # Use same base name as PDF
        structured_file = csv_file.with_stem(csv_file.stem + '_structured')
        structured_df.to_csv(structured_file, index=False, encoding='utf-8-sig')
        print(f"[OK] Structured data: {len(structured_df)} people")
        print(f"[OK] Saved to: {structured_file.name}")
        print()
    except Exception as e:
        print(f"[ERROR] Error structuring data: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Fix ই-কার encoding issues
    print("Step 5: Fixing ই-কার (ি) encoding issues...")
    try:
        import pandas as pd
        import re
        
        def fix_ikar_position(text):
            """Fix ই-কার position"""
            if not text or not isinstance(text, str):
                return text
            # Fix: "ি" + consonant → consonant + "ি" (when "ি" is not after consonant)
            text = re.sub(r'(^|\s|[\/,\.;:\(\)])ি([ক-হ])', r'\1\2ি', text)
            text = re.sub(r'(?<![ক-হ])ি([ক-হ])', r'\1ি', text)
            return text
        
        def fix_double_characters(text):
            """Fix double character issues"""
            if not text or not isinstance(text, str):
                return text
            # Common double character patterns
            fixes = [
                ('মমো', 'মো'), ('হহো', 'হো'), ('ররো', 'রো'), ('গগো', 'গো'), ('ককো', 'কো'),
                ('মমী', 'মী'), ('মমোঃ', 'মোঃ'), ('মমোছাঃ', 'মোছাঃ'), ('মমোসাঃ', 'মোসাঃ'),
                ('মমোস্ত', 'মোস্ত'), ('মমোত', 'মোত'), ('মমোজ', 'মোজ'), ('মমোল', 'মোল'),
            ]
            for double, single in fixes:
                text = text.replace(double, single)
            return text
        
        df = pd.read_csv(structured_file, encoding='utf-8-sig')
        text_columns = df.select_dtypes(include=['object']).columns
        
        ikar_fixed = 0
        double_fixed = 0
        for col in text_columns:
            # Fix ই-কার
            before_ikar = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
            df[col] = df[col].apply(fix_ikar_position)
            after_ikar = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
            ikar_fixed += (before_ikar - after_ikar)
            
            # Fix double characters
            before_double = df[col].astype(str)
            df[col] = df[col].apply(fix_double_characters)
            after_double = df[col].astype(str)
            double_fixed += (before_double != after_double).sum()
        
        # Final file with same base name
        final_file = structured_file.with_stem(structured_file.stem + '_final')
        df.to_csv(final_file, index=False, encoding='utf-8-sig')
        
        if ikar_fixed > 0:
            print(f"[OK] Fixed {ikar_fixed} ই-কার issues")
        if double_fixed > 0:
            print(f"[OK] Fixed {double_fixed} double character issues")
        if ikar_fixed == 0 and double_fixed == 0:
            print("[OK] No encoding issues found")
        print(f"[OK] Final file: {final_file.name}")
        print()
    except Exception as e:
        print(f"[WARNING] Could not fix encoding issues: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        final_file = structured_file
    
    # Summary
    print("=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print()
    print("Generated Files:")
    print(f"  1. Raw CSV: {csv_file.name}")
    print(f"  2. Structured CSV: {structured_file.name}")
    print(f"  3. Final Clean CSV: {final_file.name}")
    print()
    print(f"[FINAL] Output file: {final_file.name}")
    print()
    
    # Show sample of final data
    try:
        import pandas as pd
        df_final = pd.read_csv(final_file, encoding='utf-8-sig')
        print("Sample of final data (first 5 rows):")
        print(df_final.head(5).to_string())
        print()
    except:
        pass


if __name__ == "__main__":
    main()
