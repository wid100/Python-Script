"""
Example usage of PDF to CSV converter
"""

from pdf_to_csv import PDFToCSVConverter
from bengali_text_utils import BengaliTextProcessor, detect_bengali_text


def example_basic_conversion():
    """Basic PDF to CSV conversion example"""
    print("=== Basic Conversion Example ===")
    
    # Replace with your PDF file path
    pdf_file = "sample.pdf"
    
    try:
        converter = PDFToCSVConverter(pdf_file)
        output_file = converter.convert_to_csv_simple("output.csv")
        print(f"Successfully converted to: {output_file}")
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_file}' not found")
        print("Please provide a valid PDF file path")
    except Exception as e:
        print(f"Error: {str(e)}")


def example_text_processing():
    """Example of Bengali text processing"""
    print("\n=== Text Processing Example ===")
    
    # Sample text (replace with actual text from your PDF)
    sample_text = "এটি একটি উদাহরণ টেক্সট"
    
    processor = BengaliTextProcessor()
    cleaned_text = processor.clean_text(sample_text)
    
    print(f"Original: {sample_text}")
    print(f"Cleaned: {cleaned_text}")
    print(f"Contains Bengali: {detect_bengali_text(cleaned_text)}")


def example_custom_conversion():
    """Example with custom output path"""
    print("\n=== Custom Conversion Example ===")
    
    pdf_file = "sample.pdf"
    output_file = "my_custom_output.csv"
    
    try:
        converter = PDFToCSVConverter(pdf_file)
        converter.convert_to_csv_simple(output_file)
        print(f"Converted to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    print("PDF to CSV Converter - Example Usage\n")
    
    # Uncomment the example you want to run:
    # example_basic_conversion()
    # example_text_processing()
    # example_custom_conversion()
    
    print("\nPlease uncomment an example function to run it.")
    print("Make sure to update the PDF file path with your actual file.")
