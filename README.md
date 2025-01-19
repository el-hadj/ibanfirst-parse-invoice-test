# ibanfirst-parse-invoice-test
Interview test project for IbanFirst.
This test is about to receive an invoice and parse it to retreive a certain data extracted from this file.

## Table des matières
- [Project Structure](#structure)
- [Installation](#installation)
- [Usage](#usage)
- [Comments](#comments)


## Project Structure

    ```bash
    .
    ├── app
    │   ├── __init__.py
    │   ├── main.py               # FastAPI entry point
    │   ├── logger.py             # Logger configuration
    │   ├── models.py             # Data models
    │   ├── utils.py              # Functions for extraction
    ├── resources
    │   ├── invoice1.pdf          # Example invoices
    │   ├── invoice2.pdf
    │   └── invoice3.pdf
    ├── docker-compose.yml        # Docker Compose config
    └── requirements.txt          # List of dependencies
    ```

## Installation
1. **Clone the repository:** :

    ```bash
    git clone https://github.com/el-hadj/ibanfirst-parse-invoice-test.git

    cd project
   ```

2. **Build and run the project using Docker Compose**: First, make sure you have Docker installed. Then, use the following commands to build and run the project:


    ```bash
    docker compose up --build
   ```

3. **Swagger Interface URL**:  
   Visit the following URL to access the API's Swagger interface:
   ```bash
    http://localhost:8080/docs
   ```

## Usage
### API 1: Retrieve invoice details from a predefined file

- URL: /parse-invoice/

- Method: GET

- Parameters: file_name (options: "invoice1", "invoice2", "invoice3")

- Example request:
    ``` bash
    curl -X 'GET' 'http://127.0.0.1:8000/parse-invoice/?file_name=invoice1'
    
    ```
- Expected response (example):f

    ```json
    [
        {
            "reference": "INV-98765",
            "beneficiary_name": "ABC Corp",
            "account_id": "9876543210",
            "amount": 1000.00,
            "currency": "USD",
            "due_date": "2025-01-30"
        }
    ]

    ```

### API 2: Upload a PDF file and extract the details
- URL: /parse-invoice/upload/

- Method: POST

- Parameters: file (PDF file to upload)

- Example request:

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/parse-invoice/upload/' -F 'file=@path_to_your_invoice.pdf'
    ```
- Expected response (example):

    ```json
        [
            {
                "reference": "INV-98765",
                "beneficiary_name": "ABC Corp",
                "account_id": "9876543210",
                "amount": 1000.00,
                "currency": "USD",
                "due_date": "2025-01-30"
            }
        ]
    ```


## Comments

The second API is the best option for extracting data from an input file when the exact number of files is unknown, or for long-term use with similar files.

