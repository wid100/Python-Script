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
    while i < len(df):
        row = df.iloc[i]
        text = str(row['Text']).strip()
        page = row['Page']
        
        # Skip header lines
        if any(keyword in text for keyword in ['আদমজী', 'ক্যান্টনমেন্ট', 'এলাকা কোড', 'পৃষ্ঠা', 'ক্রিমক', 'ভাবন', 'কেন্দ্র']):
            i += 1
            continue
        
        # Check if this is a name line (starts with serial number)
        if re.match(r'^[০-৯]+\.\s+', text):
            # Extract names using pattern: number. name number. name ...
            names = []
            # Pattern: [number]. [name] followed by [number]. or end
            pattern = r'[০-৯]+\.\s+([^০-৯]+?)(?=\s+[০-৯]+\.|$)'
            matches = re.findall(pattern, text)
            for match in matches:
                name = match.strip()
                if name:
                    names.append(name)
            cleaned_names = names
            
            # Look ahead for related data (next few lines)
            voter_ids = []
            fathers = []
            mothers = []
            dob_professions = []
            addresses = []
            
            # Check next 5 lines for related data
            for j in range(1, 6):
                if i + j >= len(df):
                    break
                next_row = df.iloc[i + j]
                next_text = str(next_row['Text']).strip()
                
                if 'ভোটার নং:' in next_text and not voter_ids:
                    voter_ids = extract_sequential_data(next_text, 'ভোটার নং:')
                
                # Check for পিতা: (both correct and with encoding issues like িপতা:)
                if ('পিতা:' in next_text or 'িপতা:' in next_text) and 'মাতা:' not in next_text and not fathers:
                    # Try both patterns
                    if 'পিতা:' in next_text:
                        fathers = extract_sequential_data(next_text, 'পিতা:')
                    elif 'িপতা:' in next_text:
                        fathers = extract_sequential_data(next_text, 'িপতা:')
                
                if 'মাতা:' in next_text and not mothers:
                    mothers = extract_sequential_data(next_text, 'মাতা:')
                
                # Check for জন্মতারিখ: (both correct and with encoding issues like জন্মতািরখ:)
                if ('জন্মতারিখ:' in next_text or 'জন্মতািরখ:' in next_text) and ('পেশা:' in next_text or 'পশা:' in next_text) and not dob_professions:
                    # Normalize the text - replace encoding issues
                    normalized_text = next_text.replace('জন্মতািরখ:', 'জন্মতারিখ:').replace('পশা:', 'পেশা:')
                    
                    # Split by জন্মতারিখ: and process each part
                    parts = normalized_text.split('জন্মতারিখ:')
                    for part in parts[1:]:  # Skip first part
                        # Extract date (format: DD/MM/YYYY)
                        dob_match = re.search(r'([০-৯/]+)', part)
                        if dob_match:
                            dob = dob_match.group(1).strip()
                            # Extract profession after পেশা:
                            # Find position of পেশা: and extract everything after it until next keyword
                            prof_pos = part.find('পেশা:')
                            if prof_pos != -1:
                                # Extract text after "পেশা:"
                                prof_text = part[prof_pos + len('পেশা:'):].strip()
                                # Extract until next keyword or end
                                # Remove leading whitespace
                                prof_text = prof_text.lstrip()
                                # Extract until next জন্মতারিখ: or end of string
                                prof_match_obj = re.match(r'([^জন্মঠিকানাপেশা]+?)(?=\s+জন্মতারিখ:|ঠিকানা:|পেশা:|$)', prof_text)
                                if prof_match_obj:
                                    prof = prof_match_obj.group(1).strip()
                                else:
                                    # If no match, take everything until space or end
                                    prof = prof_text.split()[0] if prof_text.split() else ''
                                dob_professions.append({'dob': dob, 'profession': prof})
                            else:
                                # If profession not found, still add DOB
                                dob_professions.append({'dob': dob, 'profession': ''})
                
                # Check for ঠিকানা: (both correct and with encoding issues like িঠকানা:)
                if ('ঠিকানা:' in next_text or 'িঠকানা:' in next_text) and not addresses:
                    if 'ঠিকানা:' in next_text:
                        addresses = extract_sequential_data(next_text, 'ঠিকানা:')
                    elif 'িঠকানা:' in next_text:
                        addresses = extract_sequential_data(next_text, 'িঠকানা:')
            
            # Match data by index
            max_count = max(len(cleaned_names), len(voter_ids), len(fathers), 
                           len(mothers), len(dob_professions), len(addresses))
            
            for idx in range(max_count):
                structured_data.append({
                    'Name': cleaned_names[idx] if idx < len(cleaned_names) else '',
                    'NID': voter_ids[idx] if idx < len(voter_ids) else '',
                    'Father': fathers[idx] if idx < len(fathers) else '',
                    'Mother': mothers[idx] if idx < len(mothers) else '',
                    'DOB': dob_professions[idx]['dob'] if idx < len(dob_professions) else '',
                    'Profession': dob_professions[idx]['profession'] if idx < len(dob_professions) else '',
                    'Address': addresses[idx] if idx < len(addresses) else '',
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
