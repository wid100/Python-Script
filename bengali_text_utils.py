"""
Bengali Text Processing Utilities
Handles Bijoy keyboard layout issues and text cleaning
"""

import re
from typing import Dict, List


class BengaliTextProcessor:
    """Process and fix Bengali text, especially from Bijoy keyboard"""
    
    def __init__(self):
        """Initialize with common Bijoy to Unicode mappings"""
        self.bijoy_to_unicode = self._get_bijoy_mappings()
    
    def _get_bijoy_mappings(self) -> Dict[str, str]:
        """
        Get common Bijoy keyboard to Unicode mappings
        
        Returns:
            Dictionary mapping Bijoy characters to Unicode
        """
        # Common Bijoy encoding issues
        # Add more mappings as you encounter specific issues
        mappings = {
            # Add specific character fixes here
            # Example mappings (adjust based on actual issues):
            # 'à¦': 'া',  # aa kar
            # 'à§': 'ি',  # i kar
            # etc.
        }
        return mappings
    
    def fix_bijoy_text(self, text: str) -> str:
        """
        Fix Bijoy keyboard encoding issues in text
        
        Args:
            text: Text with potential Bijoy encoding issues
            
        Returns:
            Fixed Bengali text
        """
        if not text:
            return ""
        
        # Apply character mappings
        for bijoy_char, unicode_char in self.bijoy_to_unicode.items():
            text = text.replace(bijoy_char, unicode_char)
        
        # Fix common spacing issues
        text = self._fix_spacing(text)
        
        # Fix broken words (common in Bijoy keyboard)
        text = self._fix_broken_words(text)
        
        return text
    
    def _fix_spacing(self, text: str) -> str:
        """
        Fix spacing issues in Bengali text
        
        Args:
            text: Text with spacing issues
            
        Returns:
            Text with fixed spacing
        """
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([।,;:!?])', r'\1', text)
        text = re.sub(r'([।,;:!?])\s+', r'\1 ', text)
        
        return text.strip()
    
    def _fix_broken_words(self, text: str) -> str:
        """
        Fix broken words that may occur due to Bijoy keyboard issues
        
        Args:
            text: Text with potentially broken words
            
        Returns:
            Text with fixed words
        """
        # Common patterns for broken Bengali words
        # This is a basic implementation - you may need to customize
        
        # Fix words split by spaces in the middle
        # (This is a simplified approach - may need more sophisticated logic)
        
        # Remove spaces between Bengali characters that shouldn't be there
        # Bengali Unicode range: \u0980-\u09FF
        bengali_pattern = r'[\u0980-\u09FF]'
        
        # This is a placeholder - implement based on your specific issues
        # You might need to use a Bengali word segmentation library
        
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Comprehensive text cleaning for Bengali PDF text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove non-printable characters (keep Bengali Unicode)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Fix Bijoy issues
        text = self.fix_bijoy_text(text)
        
        # Normalize whitespace
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def extract_structured_data(self, text: str) -> List[Dict]:
        """
        Extract structured data from Bengali text
        
        Args:
            text: Bengali text to parse
            
        Returns:
            List of structured data dictionaries
        """
        # This is a placeholder for structured data extraction
        # Implement based on your specific PDF structure
        
        lines = text.split('\n')
        structured_data = []
        
        for idx, line in enumerate(lines):
            if line.strip():
                structured_data.append({
                    'line_number': idx + 1,
                    'content': line.strip()
                })
        
        return structured_data


def detect_bengali_text(text: str) -> bool:
    """
    Detect if text contains Bengali characters
    
    Args:
        text: Text to check
        
    Returns:
        True if Bengali text is detected
    """
    bengali_pattern = re.compile(r'[\u0980-\u09FF]')
    return bool(bengali_pattern.search(text))


def get_bengali_char_count(text: str) -> int:
    """
    Count Bengali characters in text
    
    Args:
        text: Text to analyze
        
    Returns:
        Number of Bengali characters
    """
    bengali_pattern = re.compile(r'[\u0980-\u09FF]')
    matches = bengali_pattern.findall(text)
    return len(matches)
