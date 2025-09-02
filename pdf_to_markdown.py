#!/usr/bin/env python3
"""
PDF to Markdown Converter Script

This script converts a PDF file to markdown format by extracting text
and attempting to preserve basic structure like headings and paragraphs.

Requirements:
- PyPDF2 or pypdf for PDF text extraction
- python-markdown for markdown formatting (optional)

Usage:
    python pdf_to_markdown.py input.pdf output.md
"""

import sys
import re
import argparse
from pathlib import Path

try:
    import PyPDF2
    PDF_LIBRARY = "PyPDF2"
except ImportError:
    try:
        import pypdf
        PDF_LIBRARY = "pypdf"
    except ImportError:
        print("Error: Please install PyPDF2 or pypdf:")
        print("pip install PyPDF2")
        print("or")
        print("pip install pypdf")
        sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    text = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            if PDF_LIBRARY == "PyPDF2":
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n\n<!-- Page {page_num + 1} -->\n\n"
                    text += page_text
            else:  # pypdf
                pdf_reader = pypdf.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n\n<!-- Page {page_num + 1} -->\n\n"
                    text += page_text
                    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
        
    return text


def clean_and_format_text(text):
    """Clean and format extracted text for markdown."""

    # First, let's try a different approach - collect all text and rebuild it
    lines = text.split('\n')
    all_words = []
    page_markers = []

    current_page_words = []
    current_page = None

    for line in lines:
        line = line.strip()

        if line.startswith('<!-- Page'):
            if current_page is not None and current_page_words:
                page_markers.append((current_page, current_page_words))
            current_page = line
            current_page_words = []
            continue

        if line:
            words = line.split()
            current_page_words.extend(words)

    # Don't forget the last page
    if current_page is not None and current_page_words:
        page_markers.append((current_page, current_page_words))

    # Now reconstruct text page by page
    result_lines = []

    for page_marker, words in page_markers:
        result_lines.append(page_marker)
        result_lines.append('')

        # Join all words and try to reconstruct sentences
        page_text = ' '.join(words)

        # Remove the repetitive header "Samuel Devdas, Masters Thesis 2025"
        page_text = re.sub(r'Samuel Devdas,?\s*Masters?\s*Thesis\s*2025\s*', '', page_text, flags=re.IGNORECASE)

        # Split into potential sentences
        sentences = re.split(r'([.!?]+\s+)', page_text)

        current_paragraph = []

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            # If it's just punctuation, add to previous sentence
            if re.match(r'^[.!?]+\s*$', sentence):
                if current_paragraph:
                    current_paragraph[-1] += sentence
                continue

            current_paragraph.append(sentence)

            # End paragraph on sentence endings or when it gets long
            if (sentence.endswith(('.', '!', '?')) or
                len(' '.join(current_paragraph)) > 300):

                paragraph_text = ' '.join(current_paragraph).strip()
                if paragraph_text:
                    formatted = format_paragraph(paragraph_text)
                    result_lines.append(formatted)
                    result_lines.append('')
                current_paragraph = []

        # Handle remaining text in paragraph
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph).strip()
            if paragraph_text:
                formatted = format_paragraph(paragraph_text)
                result_lines.append(formatted)
                result_lines.append('')

    # Join and clean up
    result = '\n'.join(result_lines)
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)

    return result


def format_paragraph(text):
    """Format a paragraph and detect if it should be a heading."""
    text = text.strip()
    if not text:
        return ''

    # More conservative heading detection
    words = text.split()

    # Very short text that's all caps or starts with number
    if (len(words) <= 6 and
        (text.isupper() or
         re.match(r'^\d+\.?\s+[A-Z]', text) or
         (len(words) <= 3 and text[0].isupper() and not text.endswith('.')))):

        if re.match(r'^\d+\.?\s+', text):
            return f"## {text}"
        else:
            return f"# {text}"

    # Chapter/section patterns
    elif re.match(r'^(Chapter|Section|Abstract|Introduction|Conclusion|References|Appendix)', text, re.IGNORECASE):
        return f"## {text}"

    else:
        return text


def add_markdown_metadata(title, output_text):
    """Add markdown metadata header."""
    metadata = f"""---
title: "{title}"
converted_from: PDF
conversion_date: {Path(__file__).stat().st_mtime}
---

"""
    return metadata + output_text


def convert_pdf_to_markdown(pdf_path, output_path=None):
    """Main conversion function."""
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.")
        sys.exit(1)
    
    if output_path is None:
        output_path = pdf_path.with_suffix('.md')
    else:
        output_path = Path(output_path)
    
    print(f"Converting '{pdf_path}' to '{output_path}'...")
    print(f"Using PDF library: {PDF_LIBRARY}")
    
    # Extract text from PDF
    raw_text = extract_text_from_pdf(pdf_path)
    
    if not raw_text.strip():
        print("Warning: No text extracted from PDF. The PDF might be image-based.")
        print("Consider using OCR tools like tesseract for image-based PDFs.")
        return
    
    # Clean and format text
    formatted_text = clean_and_format_text(raw_text)
    
    # Add metadata
    title = pdf_path.stem.replace('_', ' ').replace('-', ' ')
    final_text = add_markdown_metadata(title, formatted_text)
    
    # Write to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        print(f"Successfully converted to '{output_path}'")
        print(f"Output file size: {output_path.stat().st_size} bytes")
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown')
    parser.add_argument('pdf_file', help='Input PDF file path')
    parser.add_argument('output_file', nargs='?', help='Output markdown file path (optional)')
    
    args = parser.parse_args()
    
    convert_pdf_to_markdown(args.pdf_file, args.output_file)


if __name__ == "__main__":
    main()
