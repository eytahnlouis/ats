import fitz as f 
import os
import re
from docx import Document
import pytesseract
from PIL import Image
def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx file.
    """
    doc = Document(file_path) # Open the .docx file
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text) # Join all paragraphs with newlines

def extract_text_from_pdf(file_path):
    """
    Extracts text from a .pdf file.
    """
    doc = f.open(file_path) # Open the .pdf file
    text = ""
    for page in doc: # Iterate through each page
        text += page.get_text() # Extract text from the page
    return text # Return the extracted text

def extract_text_from_ocr(file_path):
    """
    Extracts text from an image file using OCR.
    """
    
    
    image = Image.open(file_path) # Open the image file
    text = pytesseract.image_to_string(image) # Perform OCR on the image
    return text # Return the extracted text

def extract_text_from_file(file_path):
    """
    Extracts text from a file based on its extension.
    """
    _, ext = os.path.splitext(file_path) # Get the file extension
    ext = ext.lower() # Convert to lowercase
    if ext == '.pdf':
        return extract_text_from_pdf(file_path) # Extract text from PDF
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        return extract_text_from_ocr(file_path)
    # Extract text from image using OCR
    elif ext == '.docx':
        return extract_text_from_docx(file_path) # Extract text from DOCX
    else:
        raise ValueError(f"Unsupported file type: {ext}") # Raise error for unsupported file types
    
if __name__ == "__main__" :
    while True:
        try:
            file_path = input("Enter the path to the file: ") # Get the file path from user
            if not os.path.exists(file_path): # Check if the file exists
                print("File does not exist. Please try again.")
                continue
            text = extract_text_from_file(file_path) # Extract text from the file
            print([text]) # Print the extracted text
            break
        except Exception as e:
            print(f"An error occurred: {e}") # Print any errors that occur