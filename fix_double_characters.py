"""
Fix double character issues in Bengali text
Example: "মমোহাম্মদ" -> "মোহাম্মদ", "হহোসেন" -> "হোসেন"
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


def fix_double_characters(text):
    """
    Fix double character issues in Bengali text
    """
    if not text or not isinstance(text, str):
        return text
    
    # Common double character patterns in Bengali
    # Fix double consonants
    double_chars = [
        ('মমো', 'মো'),
        ('হহো', 'হো'),
        ('ররো', 'রো'),
        ('গগো', 'গো'),
        ('ককো', 'কো'),
        ('মমী', 'মী'),
        ('মমোঃ', 'মোঃ'),
        ('মমোছাঃ', 'মোছাঃ'),
        ('মমোসাঃ', 'মোসাঃ'),
        ('মমোস্ত', 'মোস্ত'),
        ('মমোত', 'মোত'),
        ('মমোজ', 'মোজ'),
        ('মমোল', 'মোল'),
        ('হহো', 'হো'),
        ('ররো', 'রো'),
        ('গগো', 'গো'),
        ('ককো', 'কো'),
    ]
    
    for double, single in double_chars:
        text = text.replace(double, single)
    
    # Fix any remaining double consonants (general pattern)
    # Match: same consonant repeated (Bengali consonants)
    bengali_consonants = 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ'
    
    for consonant in bengali_consonants:
        # Fix double consonant (but not triple or more - those might be intentional)
        pattern = f'({consonant}){consonant}(?![{consonant}])'
        text = re.sub(pattern, r'\1', text)
    
    return text


def fix_csv_file(csv_path: str, output_path: str = None):
    """
    Fix double characters in CSV file
    """
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    print(f"Total rows: {len(df)}")
    
    # Fix all text columns
    text_columns = df.select_dtypes(include=['object']).columns
    
    fixed_count = 0
    for col in text_columns:
        print(f"Fixing column: {col}")
        before = df[col].astype(str)
        df[col] = df[col].apply(fix_double_characters)
        after = df[col].astype(str)
        
        # Count changes
        changes = (before != after).sum()
        if changes > 0:
            print(f"  Fixed {changes} instances in {col}")
            fixed_count += changes
    
    print(f"\nTotal fixes: {fixed_count}")
    
    # Save fixed file
    if output_path is None:
        if '_final' in csv_path:
            output_path = csv_path.replace('_final', '_final_cleaned')
        else:
            output_path = csv_path.replace('.csv', '_cleaned.csv')
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nFixed CSV saved to: {output_path}")
    
    return output_path


def main():
    """Main function"""
    # Find final CSV files
    current_dir = Path('.')
    csv_files = list(current_dir.glob('*_final.csv'))
    
    if not csv_files:
        print("No final CSV files found")
        print("Looking for structured CSV files...")
        csv_files = list(current_dir.glob('*_structured.csv'))
    
    if not csv_files:
        print("No CSV files found")
        return
    
    # Process first CSV file
    csv_file = csv_files[0]
    print(f"Processing: {csv_file.name}\n")
    
    try:
        fix_csv_file(str(csv_file))
        print("\nDone!")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
