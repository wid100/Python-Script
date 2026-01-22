"""
Automatically find and fix all CSV files in current directory
"""

import os
import glob
import pandas as pd
from pathlib import Path


def fix_bengali_characters(text):
    """Fix Bengali character encoding issues"""
    if not text or not isinstance(text, str):
        return text
    
    # Specific fixes for common patterns
    fixes = [
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
    
    for old, new in fixes:
        text = text.replace(old, new)
    
    return text


def fix_csv_file(csv_path):
    """Fix a single CSV file"""
    try:
        print(f"\nProcessing: {csv_path.name}")
        
        # Read CSV
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
        
        # Fix text columns
        text_cols = df.select_dtypes(include=['object']).columns
        fixed_count = 0
        
        for col in text_cols:
            before = df[col].astype(str).str.contains('', na=False).sum()
            df[col] = df[col].apply(fix_bengali_characters)
            after = df[col].astype(str).str.contains('', na=False).sum()
            if before > after:
                fixed_count += (before - after)
        
        # Save fixed file
        output_path = csv_path.with_stem(csv_path.stem + "_fixed")
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"  Fixed {fixed_count} issues")
        print(f"  Saved to: {output_path.name}")
        
        return True
        
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False


def main():
    """Main function"""
    import sys
    
    # Set UTF-8 for output
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Get current directory
    current_dir = Path('.')
    
    # Find all CSV files
    csv_files = list(current_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in current directory")
        return
    
    print(f"Found {len(csv_files)} CSV file(s)")
    
    # Process each CSV file
    for csv_file in csv_files:
        fix_csv_file(csv_file)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
