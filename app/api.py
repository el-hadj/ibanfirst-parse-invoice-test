import os
from typing import Literal
from app.logger import Logger
from app.utils import extract_invoice_match, extract_text_from_pdf
from fastapi import APIRouter


router = APIRouter()
logger = Logger("api_logs_file", "DEBUG").logger

@router.get("/parse-invoice/")
def parsing_invoices_files(file_name: Literal["invoice1", "invoice2", "invoice3"]):
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
