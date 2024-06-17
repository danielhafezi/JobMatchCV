import PyPDF2

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyPDF2.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: The extracted text content.
    """
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
        return text