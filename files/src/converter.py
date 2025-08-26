import os
import zipfile
import subprocess
import html2text
from datetime import datetime
import hashlib

# Requires Tesseract OCR to be installed on the system for PDF and PNG conversion.
# For Windows: https://tesseract-ocr.github.io/tessdoc/Downloads.html
# For Linux: sudo apt-get install tesseract-ocr
# For Mac: brew install tesseract

def convert_pdf_to_md(pdf_path, output_dir):
    """Converts a PDF file to Markdown using Tesseract OCR."""
    try:
        # Save output to a temporary text file first
        temp_txt_path = os.path.join(output_dir, os.path.basename(pdf_path).replace('.pdf', '.txt'))
        subprocess.run(['tesseract', pdf_path, temp_txt_path.replace('.txt', '')], check=True) # Tesseract adds .txt itself
        with open(temp_txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        md_content = f"# Converted from PDF: {os.path.basename(pdf_path)}\n\n" + content
        md_filename = os.path.basename(pdf_path).replace('.pdf', '.md')
        output_filepath = os.path.join(output_dir, md_filename)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        os.remove(temp_txt_path) # Clean up temporary text file
        print(f"Successfully converted PDF: {pdf_path} to {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error converting PDF {pdf_path}: {e}")
        return None

def convert_png_to_md(png_path, output_dir):
    """Converts a PNG image to Markdown (text from image) using Tesseract OCR."""
    try:
        temp_txt_path = os.path.join(output_dir, os.path.basename(png_path).replace('.png', '.txt'))
        subprocess.run(['tesseract', png_path, temp_txt_path.replace('.txt', '')], check=True)
        with open(temp_txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        md_content = f"# Converted from PNG: {os.path.basename(png_path)}\n\n" + content
        md_filename = os.path.basename(png_path).replace('.png', '.md')
        output_filepath = os.path.join(output_dir, md_filename)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        os.remove(temp_txt_path)
        print(f"Successfully converted PNG: {png_path} to {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error converting PNG {png_path}: {e}")
        return None

def convert_html_to_md(html_path, output_dir):
    """Converts an HTML file to Markdown."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        h = html2text.HTML2Text()
        h.ignore_links = False
        md_content = h.handle(html_content)
        md_filename = os.path.basename(html_path).replace('.html', '.md')
        output_filepath = os.path.join(output_dir, md_filename)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Converted from HTML: {os.path.basename(html_path)}\n\n" + md_content)
        print(f"Successfully converted HTML: {html_path} to {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error converting HTML {html_path}: {e}")
        return None

def extract_zip(zip_path, output_dir):
    """Extracts contents of a ZIP file to a specified directory."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"Successfully extracted ZIP: {zip_path} to {output_dir}")
        return output_dir
    except Exception as e:
        print(f"Error extracting ZIP {zip_path}: {e}")
        return None

def calculate_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def process_files_for_conversion(file_map_path, converted_dir):
    """Reads the file map, converts specified binary files, and updates the file map."""
    updated_lines = []
    with open(file_map_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = lines[0].strip().split(',')
    updated_lines.append(','.join(header) + '\n') # Add header back

    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) == len(header):
            file_path, scope, file_type, size, file_hash = parts
            original_file_path = file_path # Keep original path for source linking

            if file_type in ['pdf', 'png', 'html', 'zip']:
                converted_filepath = None
                if file_type == 'pdf':
                    converted_filepath = convert_pdf_to_md(file_path, converted_dir)
                elif file_type == 'png':
                    converted_filepath = convert_png_to_md(file_path, converted_dir)
                elif file_type == 'html':
                    converted_filepath = convert_html_to_md(file_path, converted_dir)
                elif file_type == 'zip':
                    # ZIP extraction is a bit different, it extracts multiple files
                    # We'll just mark the zip as processed and note its extraction
                    extract_zip(file_path, os.path.join(converted_dir, os.path.basename(file_path).replace('.zip', '')))
                    # We don't have a single markdown output, so we won't update file_map with a new path for the zip itself.
                    # We could rescan the extracted directory and add new entries to file_map if needed, but for now, just log.
                    print(f"ZIP file {file_path} extracted. Individual files within the ZIP are not added to file_map at this stage.")
                    converted_filepath = "N/A (extracted to directory)"

                if converted_filepath:
                    # For converted files, we update their entry in the file_map to point to the new MD file
                    # And add a header to the MD file linking to the original source
                    # The hash and size for the *original* binary file are still 'unknown' here, but can be computed if needed.
                    updated_lines.append(f"{converted_filepath},{scope},md,{size},{file_hash}\n")
                    # Also add a link to the original file in the converted MD file
                    if converted_filepath != "N/A (extracted to directory)":
                        with open(converted_filepath, 'r+', encoding='utf-8') as md_file:
                            content = md_file.read()
                            md_file.seek(0)
                            md_file.write(f"Source: [{os.path.basename(original_file_path)}](../..{original_file_path})\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nHash: {file_hash}\n\n" + content)
                else:
                    updated_lines.append(line) # If conversion failed or zip was just extracted, keep original line
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line) # Preserve malformed lines

    with open(file_map_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    print(f"Updated file map at: {file_map_path}")

if __name__ == "__main__":
    # Example usage (will be called by the agent)
    # This part will be executed when the script is run directly
    # In the agent's context, the agent will call the functions as needed
    pass
    file_map_path = "kb/file_map.csv"
    converted_dir = "docs/_converted"
    process_files_for_conversion(file_map_path, converted_dir)
