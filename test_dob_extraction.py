"""Test DOB and Profession extraction"""
import re

test_text = "জন্মতািরখ: ১২/১২/১৯৭৯ পেশা: গৃিহনী জন্মতািরখ: ৩০/০৯/১৯৭৫ পেশা: গৃিহনী জন্মতািরখ: ১০/০৪/১৯৭৩ পেশা: সরকারী চাকুরী"

# Normalize
normalized = test_text.replace('জন্মতািরখ:', 'জন্মতারিখ:')

# Try pattern
pattern = r'জন্মতারিখ:\s*([০-৯/]+)\s+পেশা:\s*([^জন্মঠিকানাপেশা]+?)(?=\s+জন্মতারিখ:|ঠিকানা:|পেশা:|$)'
matches = re.findall(pattern, normalized)

print(f"Original: {test_text}")
print(f"Normalized: {normalized}")
print(f"Matches: {matches}")

for dob, prof in matches:
    print(f"DOB: {dob}, Profession: {prof}")
