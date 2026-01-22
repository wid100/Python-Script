"""
Fix existing CSV file by removing replacement characters
"""

import pandas as pd
import sys
import io
from pathlib import Path

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def fix_replacement_characters(text):
    """Remove replacement characters from text"""
    if not text or not isinstance(text, str):
        return text
    
    # Remove Unicode replacement character (U+FFFD)
    text = text.replace('\ufffd', '')
    text = text.replace('', '')  # Also handle if it appears as empty
    
    return text

def main():
    """Main function"""
    # Find CSV files
    current_dir = Path('.')
    csv_files = list(current_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found")
        return
    
    # Process first CSV file
    csv_file = csv_files[0]
    print(f"Fixing: {csv_file.name}")
    
    try:
        # Read CSV
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        print(f"  Rows: {len(df)}")
        
        # Fix all text columns
        text_cols = df.select_dtypes(include=['object']).columns
        total_fixed = 0
        
        for col in text_cols:
            before = df[col].astype(str).str.contains('\ufffd', na=False).sum()
            df[col] = df[col].apply(fix_replacement_characters)
            after = df[col].astype(str).str.contains('\ufffd', na=False).sum()
            fixed = before - after
            if fixed > 0:
                print(f"  Column '{col}': Fixed {fixed} instances")
                total_fixed += fixed
        
        # Save fixed file (overwrite original)
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"\nTotal fixed: {total_fixed} replacement characters")
        print(f"File saved: {csv_file.name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
