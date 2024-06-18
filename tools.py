import requests
from bs4 import BeautifulSoup
import PyPDF2
import docx

from autogen import config_list_from_json
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.user_proxy_agent import UserProxyAgent

# Load environment variables
config_list = config_list_from_json("OAI_CONFIG_LIST")

def fetch_job_description(job_link: str) -> str:
    """Fetches and extracts the job description from a given URL.

    Args:
        job_link (str): The URL of the job advertisement.

    Returns:
        str: The extracted job description.
    """
    response = requests.get(job_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract text from the relevant part of the web page
        job_description = soup.get_text() 
        return job_description
    else:
        raise ValueError(f"Failed to fetch the job description. HTTP status code: {response.status_code}")

def extract_cv_text(file_path: str) -> str:
    """Extracts text content from a CV file (PDF or DOCX).

    Args:
        file_path (str): The path to the CV file.

    Returns:
        str: The extracted text content from the CV.
    
    Raises:
        ValueError: If the file format is not supported.
    """
    file_ext = file_path.split(".")[-1].lower()
    if file_ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")

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

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using python-docx.

    Args:
        file_path (str): Path to the DOCX file.

    Returns:
        str: The extracted text content.
    """
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
