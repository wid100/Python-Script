"""
Fix Bengali encoding issues - Fix ই-কার (ি) position issues
Example: "িনম্মী" → "নিম্মী", "িনশরাত" → "নিশরাত"
"""

import pandas as pd
import re
import sys
import io
from pathlib import Path

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def fix_ikar_position(text):
    """
    Fix ই-কার (ি) position issues
    Pattern: "িন" → "নি" (where ই-কার should be after consonant)
    """
    if not text or not isinstance(text, str):
        return text
    
    # Common patterns where ই-কার is in wrong position
    # Pattern: "িন" (where ই-কার is before ন) should be "নি"
    # But we need to be careful - not all "িন" are wrong
    
    # Fix specific known patterns
    fixes = [
        # "িন" patterns (ই-কার before ন)
        ('িনম্মী', 'নিম্মী'),
        ('িনশরাত', 'নিশরাত'),
        ('িনলুফা', 'নিলুফা'),
        ('িনলুফার', 'নিলুফার'),
        ('িনজাম', 'নিজাম'),
        ('িনেয়াগী', 'নেয়াগী'),
        ('িনেয়াগী', 'নেয়াগী'),
        ('িনলুফা', 'নিলুফা'),
        ('িনলুফার', 'নিলুফার'),
        ('িনরংিক', 'নিরংিক'),
        ('িনলুফার', 'নিলুফার'),
        ('িনজাম', 'নিজাম'),
        ('িনলুফা', 'নিলুফা'),
        ('িনলুফার', 'নিলুফার'),
        
        # Other common ই-কার position issues
        ('িদনার', 'দিনার'),
        ('িদলরুবা', 'দিলরুবা'),
        ('িদলরুবা', 'দিলরুবা'),
        ('িমথুন', 'মিথুন'),
        ('িনশরাত', 'নিশরাত'),
        ('িনম্মী', 'নিম্মী'),
        ('িনশরাত', 'নিশরাত'),
        ('িনলুফা', 'নিলুফা'),
        ('িনলুফার', 'নিলুফার'),
        ('িনজাম', 'নিজাম'),
        ('িনেয়াগী', 'নেয়াগী'),
        ('িনেয়াগী', 'নেয়াগী'),
        ('িনরংিক', 'নিরংিক'),
        ('িনলুফার', 'নিলুফার'),
        ('িনজাম', 'নিজাম'),
        ('িনলুফা', 'নিলুফা'),
        ('িনলুফার', 'নিলুফার'),
        
        # "িন" at start of word (most common case)
        # We'll use regex for this
    ]
    
    # Apply specific fixes
    for old, new in fixes:
        text = text.replace(old, new)
    
    # Fix general pattern: "িন" at start or after space → "নি"
    # But only if followed by consonant (not another ই-কার)
    # Pattern: start of word or after space, then "িন" followed by consonant
    text = re.sub(r'(^|\s)(িন)([ক-হ])', r'\1নি\3', text)
    
    # Fix "িন" in middle of words (more careful)
    # Only if it's clearly wrong (followed by consonant that should have ই-কার before it)
    # This is more complex, so we'll be conservative
    
    return text


def fix_all_ikar_issues(text):
    """
    Comprehensive fix for all ই-কার position issues
    """
    if not text or not isinstance(text, str):
        return text
    
    # Fix common patterns
    text = fix_ikar_position(text)
    
    # Additional common fixes
    # "িন" followed by consonant → "নি" + consonant
    # But be careful - only fix if it makes sense
    
    # Pattern: "িন" + consonant (where ই-কার should be after)
    # Common consonants that should have ই-কার after them: ন, ম, ল, etc.
    patterns = [
        (r'িন(ম)', r'নি\1'),  # "িনম" → "নিম"
        (r'িন(ল)', r'নি\1'),  # "িনল" → "নিল"
        (r'িন(জ)', r'নি\1'),  # "িনজ" → "নিজ"
        (r'িন(শ)', r'নি\1'),  # "িনশ" → "নিশ"
        (r'িন(র)', r'নি\1'),  # "িনর" → "নির"
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text


def fix_csv_file(csv_path: str, output_path: str = None):
    """
    Fix Bengali encoding issues in CSV file
    """
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    print(f"Total rows: {len(df)}")
    
    # Fix all text columns
    text_columns = df.select_dtypes(include=['object']).columns
    
    for col in text_columns:
        print(f"Fixing column: {col}")
        df[col] = df[col].apply(fix_all_ikar_issues)
    
    # Save fixed file
    if output_path is None:
        output_path = csv_path.replace('.csv', '_fixed_encoding.csv')
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nFixed CSV saved to: {output_path}")
    
    return output_path


def main():
    """Main function"""
    # Find structured CSV files
    current_dir = Path('.')
    csv_files = list(current_dir.glob('*_structured.csv'))
    
    if not csv_files:
        print("No structured CSV files found")
        print("Looking for any CSV files...")
        csv_files = list(current_dir.glob('*.csv'))
        csv_files = [f for f in csv_files if 'fixed' not in f.stem.lower()]
    
    if not csv_files:
        print("No CSV files found")
        return
    
    # Use first CSV file
    csv_file = csv_files[0]
    print(f"Processing: {csv_file.name}\n")
    
    try:
        # Fix encoding issues
        output_file = fix_csv_file(str(csv_file))
        
        print(f"\nDone! Fixed file: {output_file}")
        
        # Show sample of fixes
        print("\nSample of fixed data:")
        df = pd.read_csv(output_file, encoding='utf-8-sig')
        print(df.head(10).to_string())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
