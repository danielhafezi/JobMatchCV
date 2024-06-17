import docx

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using python-docx.

    Args:
        file_path (str): Path to the DOCX file.

    Returns:
        str: The extracted text content.
    """
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])