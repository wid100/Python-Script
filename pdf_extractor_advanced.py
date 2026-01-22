"""
Advanced PDF Text Extractor using PyMuPDF (fitz)
Better character-level extraction for accurate Bengali text
"""

import fitz  # PyMuPDF
import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Optional


class AdvancedPDFExtractor:
    """Advanced PDF text extraction with better encoding handling"""
    
    def __init__(self, pdf_path: str):
        """
        Initialize extractor with PDF file path
        
        Args:
            pdf_path: Path to the input PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def extract_text_advanced(self) -> List[Dict]:
        """
        Extract text using PyMuPDF with better encoding preservation
        
        Returns:
            List of dictionaries with page number and text
        """
        all_text_lines = []
        
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(str(self.pdf_path))
            
            print(f"Total pages: {len(doc)}")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Method 1: Extract text with layout preservation
                text_dict = page.get_text("dict")
                
                # Extract text blocks maintaining order
                blocks = []
                for block in text_dict["blocks"]:
                    if "lines" in block:  # Text block
                        block_text = ""
                        for line in block["lines"]:
                            line_text = ""
                            for span in line["spans"]:
                                # Get text with proper encoding
                                span_text = span["text"]
                                # Clean the text
                                span_text = self._clean_text(span_text)
                                if span_text.strip():
                                    line_text += span_text + " "
                            
                            if line_text.strip():
                                blocks.append(line_text.strip())
                
                # Method 2: Fallback to simple text extraction if needed
                if not blocks:
                    text = page.get_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            cleaned = self._clean_text(line)
                            if cleaned.strip():
                                blocks.append(cleaned.strip())
                
                # Add to output
                for line in blocks:
                    if line.strip():
                        all_text_lines.append({
                            'Page': page_num + 1,
                            'Text': line.strip()
                        })
            
            doc.close()
            
        except Exception as e:
            print(f"Error extracting PDF: {str(e)}")
            raise
        
        return all_text_lines
    
    def extract_text_with_ocr_fallback(self) -> List[Dict]:
        """
        Extract text with OCR fallback for scanned PDFs
        Uses PyMuPDF first, then falls back to OCR if needed
        """
        all_text_lines = []
        
        try:
            doc = fitz.open(str(self.pdf_path))
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Try text extraction first
                text = page.get_text()
                
                # If very little text extracted, might be scanned PDF
                if text and len(text.strip()) > 50:
                    # Good text extraction
                    lines = text.split('\n')
                    for line in lines:
                        cleaned = self._clean_text(line)
                        if cleaned.strip():
                            all_text_lines.append({
                                'Page': page_num + 1,
                                'Text': cleaned.strip()
                            })
                else:
                    # Try to get text blocks
                    text_dict = page.get_text("dict")
                    blocks = []
                    for block in text_dict["blocks"]:
                        if "lines" in block:
                            block_text = ""
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    span_text = span["text"]
                                    span_text = self._clean_text(span_text)
                                    if span_text.strip():
                                        block_text += span_text + " "
                            
                            if block_text.strip():
                                blocks.append(block_text.strip())
                    
                    for line in blocks:
                        if line.strip():
                            all_text_lines.append({
                                'Page': page_num + 1,
                                'Text': line.strip()
                            })
            
            doc.close()
            
        except Exception as e:
            print(f"Error in OCR fallback extraction: {str(e)}")
            raise
        
        return all_text_lines
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text while preserving Bengali characters
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove control characters but keep Bengali Unicode
        # Bengali Unicode range: U+0980-U+09FF
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove zero-width characters
        text = text.replace('\u200b', '')  # Zero-width space
        text = text.replace('\u200c', '')  # Zero-width non-joiner
        text = text.replace('\u200d', '')  # Zero-width joiner
        
        return text.strip()
    
    def extract_to_csv(self, output_path: Optional[str] = None) -> str:
        """
        Extract text and save to CSV
        
        Args:
            output_path: Optional output CSV path
            
        Returns:
            Path to created CSV file
        """
        if output_path is None:
            output_path = self.pdf_path.with_suffix('.csv')
        else:
            output_path = Path(output_path)
        
        print("Extracting text from PDF...")
        all_text_lines = self.extract_text_advanced()
        
        if all_text_lines:
            df = pd.DataFrame(all_text_lines)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"CSV created: {output_path}")
            print(f"Total lines: {len(df)}")
            return str(output_path)
        else:
            raise ValueError("No text extracted from PDF")


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor_advanced.py <pdf_file> [output_csv]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        extractor = AdvancedPDFExtractor(pdf_path)
        extractor.extract_to_csv(output_path)
        print("\nExtraction completed successfully!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
