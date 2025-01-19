from typing import Literal
from app.logger import Logger
from app.utils import extract_contents, extract_invoice_match, extract_text_from_pdf
from fastapi import APIRouter, File, UploadFile


router = APIRouter()
logger = Logger("api_logs_file", "DEBUG").logger

@router.get("/parse-invoice/")
def parsing_invoices_files(file_name: Literal["invoice1", "invoice2", "invoice3"]):
    """
    Parses an invoice PDF file from the server's 'resources/invoices/' directory 
    based on the provided file name.

    Args:
    -----
        file_name (Literal["invoice1", "invoice2", "invoice3"]): The name of the invoice file 
        to be parsed (without the '.pdf' extension). The file name must be one of 
        'invoice1', 'invoice2', or 'invoice3'.

    Returns:
    --------
        List[dict[]]: A list of parsed invoice information extracted from the PDF file.

    """
    try:
        file_path = f"resources/invoices/{file_name}.pdf"
        extracted_text = extract_text_from_pdf(file_path, logger)
    
        result = []
        for text in extracted_text:
            invoice = extract_invoice_match(text)
            result.append(invoice)
        logger.info(f" size of result: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"parsing_invoices_files error : {e}")
        raise e
    

@router.post("/parse-invoice/upload/")
async def parsing_invoices_files(file: UploadFile = File(...)):
    """
    Parses an uploaded invoice PDF file and extracts the relevant invoice details.

    Args:
    -----
        file (UploadFile): The invoice PDF file uploaded by the user.

    Returns:
    -------
        List[dict]: A list of parsed invoice information extracted from the uploaded file.
    
    """
    try:

        contents = await file.read()
        extracted_text = extract_contents(contents, logger)
    
        result = []
        for text in extracted_text:
            invoice = extract_invoice_match(text)
            result.append(invoice)
        logger.info(f" size of result: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"parsing_invoices_files error : {e}")
        raise e
