from app.logger import Logger
from fastapi import FastAPI
from app.api import router


app = FastAPI(
        title="IBAN FIRST TEST",
        description="",
        summary="App for IBAN CUSTOMER",
        version="1.0.0",
        license_info = {
            "name": "ELHADJ Software",
            "url": "https://google.fr/",
        },
)

app.include_router(router)





