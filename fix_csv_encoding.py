"""
Fix encoding issues in CSV file - Replace characters with correct Bengali text
"""

import pandas as pd
import re
from pathlib import Path


def fix_bengali_characters(text):
    """
    Fix common Bengali character encoding issues
    Replace characters with correct Bengali characters based on context
    """
    if not text or not isinstance(text, str):
        return text
    
    # First, fix specific known patterns (order matters - longer patterns first)
    specific_fixes = [
        # ভোটার related
        ('ভাটার', 'ভোটার'),
        
        # কোড related  
        ('কাড', 'কোড'),
        
        # রোড related
        ('রাড', 'রোড'),
        
        # মোঃ related
        ('মাহাম্মদ', 'মোহাম্মদ'),
        ('মাসােদ্দক', 'মোসাদ্দেক'),
        ('মাসাম্মৎ', 'মোসাম্মৎ'),
        ('মাসাম্মত', 'মোসাম্মত'),
        ('মাসিলম', 'মোছলিম'),
        ('মাহাঃ', 'মোহাঃ'),
        ('মাসাঃ', 'মোসাঃ'),
        ('মাছাঃ', 'মোছাঃ'),
        ('মাঃ', 'মোঃ'),
        
        # বেগম related
        ('বগম', 'বেগম'),
        
        # পেশা related
        ('পশা', 'পেশা'),
        
        # কেন্দ্র related
        ('কন্দ্র', 'কেন্দ্র'),
        
        # সয়দা related
        ('সয়দা', 'সয়দা'),
        ('সয়দ', 'সয়দ'),
        
        # খোদেজা related
        ('খােদজা', 'খোদেজা'),
        
        # জোবেদা related
        ('জােবদা', 'জোবেদা'),
        
        # নওয়াজ related
        ('নওয়াজ', 'নওয়াজ'),
        
        # গোলাম related
        ('গালাম', 'গোলাম'),
        
        # ফরিদৌসী related
        ('ফরেদৌসী', 'ফরিদৌসী'),
        
        # শেখ related
        ('শখ', 'শেখ'),
        
        # রেজাউল related
        ('রজওয়ানা', 'রেজওয়ানা'),
        ('রজাউল', 'রেজাউল'),
        
        # হোসেন related
        ('হােসন', 'হোসেন'),
        
        # Additional common fixes
        ('কায়াটার', 'কোয়ার্টার'),
        ('কায়াটা', 'কোয়ার্টার'),
        ('কায়াট', 'কোয়ার্টার'),
        ('গালস', 'গার্লস'),
        ('টচার', 'টিচার'),
    ]
    
    # Apply specific fixes
    for old, new in specific_fixes:
        text = text.replace(old, new)
    
    # Now fix standalone characters based on context
    # Pattern: [consonant][replacement_char][consonant] -> [consonant]ো[consonant] or [consonant]ে[consonant]
    # Common patterns:
    # - ভা -> ভো (when followed by টার, etc.)
    # - ক -> কো (when followed by ড, etc.)
    # - র -> রো (when followed by ড, etc.)
    # - মা -> মো (when followed by ঃ, etc.)
    # - ব -> বে (when followed by গম, etc.)
    # - প -> পে (when followed by শা, etc.)
    # - ক -> কে (when followed by ন্দ্র, etc.)
    
    # Context-based fixes for character
    context_fixes = [
        # ভো pattern
        (r'ভ([ক-হ])', r'ভো\1'),
        # কো pattern  
        (r'ক([ক-হ])', r'কো\1'),
        # রো pattern
        (r'র([ক-হ])', r'রো\1'),
        # মো pattern
        (r'মা([ঃ-হ])', r'মো\1'),
        (r'মা([ক-হ])', r'মো\1'),
        # বে pattern
        (r'ব([ক-হ])', r'বে\1'),
        # পে pattern
        (r'প([ক-হ])', r'পে\1'),
        # কে pattern (for কেন্দ্র)
        (r'ক([ন-হ])', r'কে\1'),
    ]
    
    # Apply context-based fixes
    for pattern, replacement in context_fixes:
        text = re.sub(pattern, replacement, text)
    
    return text


def fix_csv_file(input_csv_path, output_csv_path=None):
    """
    Fix encoding issues in CSV file
    
    Args:
        input_csv_path: Path to input CSV file
        output_csv_path: Path to output CSV file (if None, overwrites input)
    """
    input_path = Path(input_csv_path)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_csv_path}")
        return
    
    if output_csv_path is None:
        output_csv_path = input_path.with_stem(input_path.stem + "_fixed")
    
    print(f"Reading CSV file: {input_path}")
    
    try:
        # Read CSV with UTF-8 encoding
        df = pd.read_csv(input_path, encoding='utf-8-sig')
        
        print(f"Total rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Fix all text columns
        text_columns = df.select_dtypes(include=['object']).columns
        
        for col in text_columns:
            print(f"Fixing column: {col}")
            df[col] = df[col].apply(fix_bengali_characters)
        
        # Count remaining characters
        remaining_issues = 0
        for col in text_columns:
            if df[col].dtype == 'object':
                remaining_issues += df[col].astype(str).str.contains('', na=False).sum()
        
        print(f"\nRemaining characters: {remaining_issues}")
        
        # Save fixed CSV
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"\nFixed CSV saved to: {output_csv_path}")
        
        return output_csv_path
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function"""
    import sys
    import glob
    import os
    
    # Set UTF-8 encoding for stdout
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    if len(sys.argv) < 2:
        # Try to find CSV files in current directory
        csv_files = glob.glob("*.csv")
        if csv_files:
            print("Found CSV files in current directory:")
            for i, f in enumerate(csv_files, 1):
                try:
                    print(f"  {i}. {f}")
                except:
                    print(f"  {i}. [File with special characters]")
            print(f"\nUsing first file: {csv_files[0]}")
            input_file = csv_files[0]
        else:
            print("Usage: python fix_csv_encoding.py <csv_file> [output_file]")
            print("\nExample:")
            print("  python fix_csv_encoding.py input.csv")
            print("  python fix_csv_encoding.py input.csv output_fixed.csv")
            sys.exit(1)
    else:
        input_file = sys.argv[1]
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    fix_csv_file(input_file, output_file)
    print("\nDone!")


if __name__ == "__main__":
    main()
