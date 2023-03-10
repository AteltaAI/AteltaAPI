import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ateltaapi.routes import main_router

description = """Welcome to AteltaAPI version: 0.0.1, This is our first release of
our API which internally uses ateltaSDK, and provides functionality for pose matching
and other evaluation metrics.
"""

app = FastAPI(
    title="ateltaapi",
    description=description,
    version="0.0.1",
    terms_of_service="http://ateltaapi.com/terms/",
    contact={
        "name": "AteltaAI",
        "url": "http://ateltaapi.com/contact/",
        "email": "AteltaAI@ateltaapi.com",
    },
    license_info={"name": "The Unlicense", "url": "https://unlicense.org",},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(main_router)


@app.on_event("startup")
def on_startup(): 
    ...


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
