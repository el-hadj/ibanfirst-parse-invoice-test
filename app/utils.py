from datetime import datetime, timedelta
from decimal import Decimal
import re
import PyPDF2
from app.models import Invoice

def extract_text_from_pdf(pdf_file: str, logger) -> list:
    try:
        logger.info(f"Extracting this file name: {pdf_file}")
        with open(pdf_file, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pdf_text = []

            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)

            return pdf_text
    except Exception as e:
        logger.error(f"extract_text_from_pdf error : {e} ")
        raise e
    

def extract_invoice_match(text: str) -> Invoice:
    try:
        reference_match = re.search(r"Invoice #: \s*([\w\-]+)", text)
        account_id_match = re.search(r"Account #: \s*([\w\d]+)", text)
        amount_match = re.search(r"Total: \s*([\d,\.]+)\s*(\w+)?", text)
        received_at_match = re.search(r" Received At: \s*([\w\s\d]+)", text)
        payments_date_match = re.search(r"Please pay this invoice within (\d+) days after the reception date", text)
        beneficiary_match = re.search(r"ABC Corp | [\w\d\s]+ Corp", text)

        received_at = (
            datetime.strptime(received_at_match.group(1), "%d %B %Y")
            if received_at_match
            else None
        )

        due_date = None
        if received_at and payments_date_match:
            days_to_add = int(payments_date_match.group(1))
            due_date = received_at + timedelta(days=days_to_add)

        invoice = Invoice(
            reference=reference_match.group(1) if reference_match else None,
            beneficiary_name=beneficiary_match.group(0) if beneficiary_match else None,
            account_id=account_id_match.group(1) if account_id_match else None,
            amount=Decimal(amount_match.group(1)) if amount_match else None,
            currency=amount_match.group(2) if amount_match and amount_match.group(2) else None,
            due_date=due_date,
        )

        return invoice
    except Exception as e:
        raise ValueError(f"Error parsing invoice details: {e}")