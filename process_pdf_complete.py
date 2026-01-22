"""
Complete PDF to CSV Processing Pipeline
1. Convert PDF to CSV
2. Fix encoding issues (replacement characters)
3. Structure voter data
4. Fix ই-কার encoding issues
5. Generate final clean CSV
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
    
    # Step 1: Find PDF file
    print("Step 1: Finding PDF file...")
    current_dir = Path('.')
    pdf_files = list(current_dir.glob('*.pdf'))
    
    if not pdf_files:
        print("❌ No PDF files found in current directory")
        return
    
    pdf_file = pdf_files[0]
    try:
        print(f"[OK] Found PDF: {pdf_file.name}")
    except:
        print(f"[OK] Found PDF file")
    print()
    
    # Step 2: Convert PDF to CSV
    print("Step 2: Converting PDF to CSV...")
    try:
        from pdf_to_csv import PDFToCSVConverter
        import pdfplumber
        import pandas as pd
        
        # Convert PDF to CSV directly
        converter = PDFToCSVConverter(str(pdf_file))
        
        # Extract text
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
        
        # Save to CSV
        csv_file = Path(pdf_file).with_suffix('.csv')
        if all_text_lines:
            df = pd.DataFrame(all_text_lines)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"[OK] CSV created: {len(df)} lines")
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
        
        structured_df = structure_voter_data(csv_file)
        structured_file = Path(csv_file).with_stem(Path(csv_file).stem + '_structured')
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
        
        df = pd.read_csv(structured_file, encoding='utf-8-sig')
        text_columns = df.select_dtypes(include=['object']).columns
        
        fixed_count = 0
        for col in text_columns:
            before = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
            df[col] = df[col].apply(fix_ikar_position)
            after = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
            fixed_count += (before - after)
        
        final_file = structured_file.with_stem(structured_file.stem + '_final')
        df.to_csv(final_file, index=False, encoding='utf-8-sig')
        
        if fixed_count > 0:
            print(f"[OK] Fixed {fixed_count} ই-কার issues")
        else:
            print("[OK] No ই-কার issues found")
        print(f"[OK] Final file: {final_file.name}")
        print()
    except Exception as e:
        print(f"[WARNING] Could not fix ই-কার issues: {str(e)}")
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
    print(f"  1. Raw CSV: {Path(csv_file).name}")
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
