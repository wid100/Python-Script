"""
Structure voter data from CSV into individual rows
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


def extract_names(line: str) -> List[str]:
    """Extract names from a line like '১. ফাতেমা দিনার সালাউদ্দীন ২. শাহ্ নাজ সুলতানা ৩. নাজমা আকতার'"""
    names = []
    # Pattern: number followed by name (Bengali numerals: ১-৯, ১০-৯৯, etc.)
    pattern = r'[০-৯]+\.\s*([^০-৯]+?)(?=\s+[০-৯]+\.|$)'
    matches = re.findall(pattern, line)
    for match in matches:
        name = match.strip()
        if name:
            names.append(name)
    return names


def extract_voter_ids(line: str) -> List[str]:
    """Extract voter IDs from a line like 'ভোটার নং: ২৬২২০১২৩০০০১ ভোটার নং: ২৬২২০১২৩০০০৩'"""
    ids = []
    pattern = r'ভোটার\s+নং:\s*([০-৯]+)'
    matches = re.findall(pattern, line)
    return matches


def extract_fathers(line: str) -> List[str]:
    """Extract father names from a line like 'পিতা: আবু তাহের মোঃ সালাউদ্দীন পিতা: আব্দুর রাজ্জাক মজুমদার'"""
    fathers = []
    # Split by 'পিতা:' and extract each father name
    parts = re.split(r'পিতা:\s*', line)
    for part in parts[1:]:  # Skip first empty part
        # Extract until next keyword or end
        match = re.match(r'([^পিতামাতাজন্মঠিকানাপেশা]+?)(?=\s+পিতা:|মাতা:|জন্ম|ঠিকানা:|পেশা:|$)', part)
        if match:
            father = match.group(1).strip()
            if father:
                fathers.append(father)
    return fathers


def extract_mothers(line: str) -> List[str]:
    """Extract mother names from a line like 'মাতা: দিলরুবা সালাউদ্দীন মাতা: ফাতেমা মজুমদার'"""
    mothers = []
    # Split by 'মাতা:' and extract each mother name
    parts = re.split(r'মাতা:\s*', line)
    for part in parts[1:]:  # Skip first empty part
        # Extract until next keyword or end
        match = re.match(r'([^পিতামাতাজন্মঠিকানাপেশা]+?)(?=\s+পিতা:|মাতা:|জন্ম|ঠিকানা:|পেশা:|$)', part)
        if match:
            mother = match.group(1).strip()
            if mother:
                mothers.append(mother)
    return mothers


def extract_dob_profession(line: str) -> List[Dict[str, str]]:
    """Extract DOB and Profession pairs from a line"""
    results = []
    # Pattern: জন্মতারিখ: DD/MM/YYYY পেশা: Profession
    # More flexible pattern
    pattern = r'জন্মতারিখ:\s*([০-৯/]+)\s+পেশা:\s*([^জন্মঠিকানাপেশা]+?)(?=\s+জন্মতারিখ:|ঠিকানা:|পেশা:|$)'
    matches = re.findall(pattern, line)
    for dob, prof in matches:
        results.append({
            'dob': dob.strip(),
            'profession': prof.strip()
        })
    return results


def extract_addresses(line: str) -> List[str]:
    """Extract addresses from a line"""
    addresses = []
    # Split by 'ঠিকানা:' and extract each address
    parts = re.split(r'ঠিকানা:\s*', line)
    for part in parts[1:]:  # Skip first empty part
        # Extract until next keyword or end
        match = re.match(r'([^পিতামাতাজন্মঠিকানাপেশা]+?)(?=\s+পিতা:|মাতা:|জন্ম|ঠিকানা:|পেশা:|$)', part)
        if match:
            address = match.group(1).strip()
            if address:
                addresses.append(address)
    return addresses


def structure_voter_data(csv_path: str) -> pd.DataFrame:
    """
    Read CSV and structure voter data into individual rows
    """
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    print(f"Total lines in CSV: {len(df)}")
    
    # Group data by page - collect all lines for a page
    structured_data = []
    
    # Group lines by page
    pages_data = {}
    for idx, row in df.iterrows():
        text = str(row['Text']).strip()
        page = row['Page']
        
        # Skip header lines
        if any(keyword in text for keyword in ['আদমজী', 'ক্যান্টনমেন্ট', 'এলাকা কোড', 'পৃষ্ঠা', 'ক্রিমক', 'ভাবন']):
            continue
        
        if page not in pages_data:
            pages_data[page] = []
        pages_data[page].append(text)
    
    # Process each page
    for page, lines in pages_data.items():
        # Find name lines (contain serial numbers)
        name_lines = [l for l in lines if re.search(r'^[০-৯]+\.\s+', l)]
        
        # Find voter ID lines
        voter_lines = [l for l in lines if 'ভোটার নং:' in l]
        
        # Find father lines
        father_lines = [l for l in lines if 'পিতা:' in l and 'মাতা:' not in l]
        
        # Find mother lines
        mother_lines = [l for l in lines if 'মাতা:' in l]
        
        # Find DOB/Profession lines
        dob_prof_lines = [l for l in lines if 'জন্মতারিখ:' in l and 'পেশা:' in l]
        
        # Find address lines
        address_lines = [l for l in lines if 'ঠিকানা:' in l]
        
        # Extract all data
        all_names = []
        all_voter_ids = []
        all_fathers = []
        all_mothers = []
        all_dob_profs = []
        all_addresses = []
        
        for line in name_lines:
            all_names.extend(extract_names(line))
        
        for line in voter_lines:
            all_voter_ids.extend(extract_voter_ids(line))
        
        for line in father_lines:
            all_fathers.extend(extract_fathers(line))
        
        for line in mother_lines:
            all_mothers.extend(extract_mothers(line))
        
        for line in dob_prof_lines:
            all_dob_profs.extend(extract_dob_profession(line))
        
        for line in address_lines:
            all_addresses.extend(extract_addresses(line))
        
        # Match data by index
        max_count = max(len(all_names), len(all_voter_ids), len(all_fathers), 
                       len(all_mothers), len(all_dob_profs), len(all_addresses))
        
        for i in range(max_count):
            structured_data.append({
                'Name': all_names[i] if i < len(all_names) else '',
                'NID': all_voter_ids[i] if i < len(all_voter_ids) else '',
                'Father': all_fathers[i] if i < len(all_fathers) else '',
                'Mother': all_mothers[i] if i < len(all_mothers) else '',
                'DOB': all_dob_profs[i]['dob'] if i < len(all_dob_profs) else '',
                'Profession': all_dob_profs[i]['profession'] if i < len(all_dob_profs) else '',
                'Address': all_addresses[i] if i < len(all_addresses) else '',
                'Page': page
            })
    
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
        print("\nFirst few rows:")
        print(structured_df.head(10).to_string())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
