from datetime import datetime, timedelta
from decimal import Decimal
import io
import re
from PyPDF2 import PdfReader
from app.models import Invoice

def extract_text_from_pdf(pdf_file: str, logger) -> list:
    try:
        logger.info(f"Extracting this file name: {pdf_file}")
        with open(pdf_file, 'rb') as pdf:
            reader = PdfReader(pdf, strict=False)
            pdf_text = []

            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)

            return pdf_text
    except Exception as e:
        logger.error(f"extract_text_from_pdf error : {e} ")
        raise e


def extract_contents(pdf_file_contents, logger) -> list:
    try:
        logger.info("Extracting text from PDF content")
        pdf_text = []

        pdf_file = io.BytesIO(pdf_file_contents)
        reader = PdfReader(pdf_file, strict=False)

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
        received_at_match = re.search(
            r"Received At: (\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4})",
            text
        )
        payments_date_match = re.search(r"Please pay this invoice within (\d+) days after the reception date", text)
        beneficiary_match = re.search(r"Account #:\s+[A-Za-z0-9]+[\s\n]+([A-Za-z\s]+Corp)", text, re.DOTALL)
        due_match_date = re.search(r"Due: (\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", text)
        
        due_date = None
        if due_match_date:
            date_str = due_match_date.group(1)
            due_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            received_at_str = received_at_match.group(1)
            received_at_date = datetime.strptime(received_at_str, "%d %B %Y").date()
            payment_days = int(payments_date_match.group(1))
            print(f"received_at_date :{received_at_date}, payment_days: {payment_days}")
            due_date = received_at_date + timedelta(days=payment_days)


        invoice = Invoice(
            reference=reference_match.group(1) if reference_match else None,
            beneficiary_name=beneficiary_match.group(1).strip() if beneficiary_match else None,
            account_id=account_id_match.group(1) if account_id_match else None,
            amount=Decimal(amount_match.group(1)) if amount_match else None,
            currency=amount_match.group(2) if amount_match and amount_match.group(2) else None,
            due_date=due_date if due_date else None,
        )

        return invoice
    except Exception as e:
        raise ValueError(f"Error parsing invoice details: {e}")