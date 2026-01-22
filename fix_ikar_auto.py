"""
Automatically fix ই-কার (ি) position issues
Detects "ি" before consonants and moves it after the consonant
Example: "িব" → "বি", "িশ" → "শি", "িম" → "মি"
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
    Automatically fix ই-কার (ি) position
    Only fix "ি" that appears BEFORE consonants (wrong position)
    Strategy: Only fix "ি" + consonant when "ি" is NOT preceded by a consonant
    This way we don't break correct patterns like "কি", "মি", etc.
    """
    if not text or not isinstance(text, str):
        return text
    
    # Strategy: Only fix "ি" + consonant when "ি" is clearly in wrong position
    # Wrong position: "ি" is at start, after space/punctuation, or after vowel/modifier (but NOT after consonant)
    # Correct position: consonant + "ি" (we don't want to touch these)
    
    # Pattern 1: "ি" at start of text or after space/punctuation, followed by consonant
    # This is definitely wrong: "িব" → "বি", "৬৬/িব" → "৬৬/বি"
    text = re.sub(r'(^|\s|[\/,\.;:\(\)])ি([ক-হ])', r'\1\2ি', text)
    
    # Pattern 2: "ি" after a vowel (but not after consonant)
    # Bengali vowels: অ, আ, ই, ঈ, উ, ঊ, এ, ঐ, ও, ঔ
    # This will fix: "সুিফয়া" → "সুফিয়া"
    # But we need to make sure we don't fix if there's a consonant before "ি"
    
    # More careful: Fix "ি" + consonant only if "ি" is NOT preceded by a consonant
    # Pattern: (not consonant) + "ি" + consonant → (not consonant) + consonant + "ি"
    # This means: fix when "ি" is at start, after vowel, after modifier, after space, etc.
    # But NOT when "ি" is after a consonant (that would be correct like "কি")
    
    # Use negative lookbehind to ensure "ি" is NOT after a consonant
    # Pattern: (not [ক-হ]) + "ি" + [ক-হ] → (not [ক-হ]) + [ক-হ] + "ি"
    # This will fix wrong ones but leave correct ones alone
    text = re.sub(r'(?<![ক-হ])ি([ক-হ])', r'\1ি', text)
    
    return text


def fix_all_ikar_issues(text):
    """
    Comprehensive fix for all ই-কার position issues
    """
    if not text or not isinstance(text, str):
        return text
    
    # First, fix the general pattern: "ি" + consonant → consonant + "ি"
    text = fix_ikar_position(text)
    
    # Additional specific fixes for common cases
    # These are patterns we know are definitely wrong
    
    return text


def fix_csv_file(csv_path: str, output_path: str = None):
    """
    Fix ই-কার encoding issues in CSV file
    """
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    print(f"Total rows: {len(df)}")
    
    # Fix all text columns
    text_columns = df.select_dtypes(include=['object']).columns
    
    fixed_count = 0
    for col in text_columns:
        print(f"Fixing column: {col}")
        # Count issues before
        before = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
        df[col] = df[col].apply(fix_all_ikar_issues)
        # Count issues after
        after = df[col].astype(str).str.contains('ি[ক-হ]', na=False).sum()
        fixed = before - after
        if fixed > 0:
            print(f"  Fixed {fixed} instances in {col}")
            fixed_count += fixed
    
    print(f"\nTotal fixes: {fixed_count}")
    
    # Save fixed file
    if output_path is None:
        # Replace _fixed_encoding with _final or add _final
        if '_fixed_encoding' in csv_path:
            output_path = csv_path.replace('_fixed_encoding', '_final')
        else:
            output_path = csv_path.replace('.csv', '_final.csv')
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nFixed CSV saved to: {output_path}")
    
    return output_path


def main():
    """Main function"""
    # Find structured CSV files (prefer fixed_encoding, then structured)
    current_dir = Path('.')
    csv_files = list(current_dir.glob('*_fixed_encoding.csv'))
    
    if not csv_files:
        csv_files = list(current_dir.glob('*_structured.csv'))
    
    if not csv_files:
        print("No structured CSV files found")
        print("Looking for any CSV files...")
        csv_files = list(current_dir.glob('*.csv'))
        csv_files = [f for f in csv_files if 'final' not in f.stem.lower()]
    
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
