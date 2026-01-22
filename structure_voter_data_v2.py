"""
Structure voter data from CSV into individual rows - Improved version
Each person gets one row with: Name, NID, Father, Mother, DOB, Address, Profession
"""

import pandas as pd
import re
import sys
import io
from pathlib import Path
from typing import List, Dict

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def extract_sequential_data(text: str, keyword: str) -> List[str]:
    """Extract data that appears multiple times with same keyword"""
    results = []
    # Split by keyword and extract each occurrence
    parts = text.split(keyword)
    for part in parts[1:]:  # Skip first part before first keyword
        # Extract until next keyword or end of string
        # Look for next keyword pattern - be more specific
        match = re.match(r'^\s*([^পিতামাতাজন্মঠিকানাপেশাভোটার]+?)(?=\s+(?:পিতা:|মাতা:|জন্মতারিখ:|ঠিকানা:|পেশা:|ভোটার\s+নং:)|$)', part, re.DOTALL)
        if match:
            value = match.group(1).strip()
            if value:
                results.append(value)
        else:
            # If no match, take everything until end or next obvious separator
            value = part.strip()
            if value:
                results.append(value)
    return results


def structure_voter_data(csv_path: str) -> pd.DataFrame:
    """
    Read CSV and structure voter data into individual rows
    """
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    print(f"Total lines in CSV: {len(df)}")
    
    structured_data = []
    
    # Process line by line, grouping related data
    i = 0
    name_count = 0
    while i < len(df):
        row = df.iloc[i]
        text = str(row['Text']).strip()
        page = row['Page']
        
        # Skip header lines
        if any(keyword in text for keyword in ['আদমজী', 'ক্যান্টনমেন্ট', 'এলাকা কোড', 'পৃষ্ঠা', 'ক্রিমক', 'ভাবন', 'কেন্দ্র', 'শহীদ রমিজ']):
            i += 1
            continue
        
        # Check if this is a name line (starts with serial number like "১ ." or "১.")
        # Pattern: Bengali number followed by dot and space, then name
        # Try multiple patterns
        name_match = None
        patterns = [
            r'^[০-৯]+\.\s+(.+)$',  # "১ . name"
            r'^[০-৯]+\.\s*(.+)$',  # "১. name" or "১ . name"
            r'^[০-৯]+\s*\.\s*(.+)$',  # "১ . name" with flexible spacing
        ]
        
        for pattern in patterns:
            name_match = re.match(pattern, text)
            if name_match:
                break
        if name_match:
            # Extract name
            name = name_match.group(1).strip()
            
            # Initialize data for this person
            voter_id = ''
            father = ''
            mother = ''
            dob = ''
            profession = ''
            address = ''
            
            # Look ahead for related data (next 5-6 lines)
            for j in range(1, 7):
                if i + j >= len(df):
                    break
                next_row = df.iloc[i + j]
                next_text = str(next_row['Text']).strip()
                
                # Check if we hit next person (starts with number)
                if re.match(r'^[০-৯]+\.\s+', next_text):
                    break
                
                # Extract ভোটার নং
                if 'ভোটার নং:' in next_text and not voter_id:
                    match = re.search(r'ভোটার\s+নং:\s*([০-৯]+)', next_text)
                    if match:
                        voter_id = match.group(1).strip()
                
                # Extract পিতা
                if ('পিতা:' in next_text or 'িপতা:' in next_text) and not father:
                    # Normalize
                    normalized = next_text.replace('িপতা:', 'পিতা:')
                    match = re.search(r'পিতা:\s*(.+?)(?=\s*(?:মাতা:|জন্মতারিখ:|ঠিকানা:|পেশা:|$))', normalized)
                    if match:
                        father = match.group(1).strip()
                
                # Extract মাতা
                if 'মাতা:' in next_text and not mother:
                    match = re.search(r'মাতা:\s*(.+?)(?=\s*(?:জন্মতারিখ:|ঠিকানা:|পেশা:|ভোটার\s+নং:|$))', next_text)
                    if match:
                        mother = match.group(1).strip()
                
                # Extract জন্মতারিখ and পেশা
                if ('জন্মতারিখ:' in next_text or 'জন্মতািরখ:' in next_text) and not dob:
                    # Normalize
                    normalized = next_text.replace('জন্মতািরখ:', 'জন্মতারিখ:').replace('পশা:', 'পেশা:')
                    
                    # Extract DOB
                    dob_match = re.search(r'জন্মতারিখ:\s*([০-৯/]+)', normalized)
                    if dob_match:
                        dob = dob_match.group(1).strip()
                    
                    # Extract Profession
                    prof_match = re.search(r'পেশা:\s*(.+?)(?=\s*(?:ঠিকানা:|জন্মতারিখ:|$))', normalized)
                    if prof_match:
                        profession = prof_match.group(1).strip()
                
                # Extract ঠিকানা
                if ('ঠিকানা:' in next_text or 'িঠকানা:' in next_text) and not address:
                    # Normalize
                    normalized = next_text.replace('িঠকানা:', 'ঠিকানা:')
                    match = re.search(r'ঠিকানা:\s*(.+?)(?=\s*(?:ভোটার\s+নং:|পিতা:|মাতা:|জন্মতারিখ:|পেশা:|$))', normalized)
                    if match:
                        address = match.group(1).strip()
            
            # Add structured data for this person
            if name:  # Only add if we have at least a name
                structured_data.append({
                    'Name': name,
                    'NID': voter_id,
                    'Father': father,
                    'Mother': mother,
                    'DOB': dob,
                    'Profession': profession,
                    'Address': address,
                    'Page': page
                })
        
        i += 1
    
    result_df = pd.DataFrame(structured_data)
    print(f"\nStructured data: {len(result_df)} people")
    return result_df


def main():
    """Main function"""
    # Find CSV files in current directory
    current_dir = Path('.')
    csv_files = list(current_dir.glob('*.csv'))
    
    # Filter out already structured files
    csv_files = [f for f in csv_files if 'structured' not in f.stem.lower() and 'fixed' not in f.stem.lower()]
    
    if not csv_files:
        print("No CSV files found")
        return
    
    # Use first CSV file
    csv_file = csv_files[0]
    print(f"Processing: {csv_file.name}\n")
    
    try:
        # Structure the data
        structured_df = structure_voter_data(str(csv_file))
        
        # Save structured CSV
        output_file = csv_file.with_stem(csv_file.stem + '_structured')
        structured_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\nStructured CSV saved to: {output_file.name}")
        print(f"Total people: {len(structured_df)}")
        print("\nFirst few rows with data:")
        # Show rows that have at least some data filled
        sample_df = structured_df[structured_df['Father'].notna() & (structured_df['Father'] != '')].head(5)
        if len(sample_df) > 0:
            print(sample_df.to_string())
        else:
            print(structured_df.head(10).to_string())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
