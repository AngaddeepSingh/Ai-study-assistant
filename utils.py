import pypdf
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(uploaded_file) -> str:
    """Reads an uploaded PDF file and extracts all text."""
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_url(url: str) -> str:
    """Fetches a webpage URL and extracts the main text content."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Parse HTML and remove clutter (scripts, styles, navbars)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(["script", "style", "nav", "footer"]):
        script_or_style.decompose()
        
    return soup.get_text(separator=' ', strip=True)