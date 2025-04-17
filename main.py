from fastapi import FastAPI, Request, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging
import os
from dotenv import load_dotenv

app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sso-app")

origins = [
    "http://localhost:8080",  # or whatever your frontend runs on
    "https://wordpress-bakuriani-tst.mth.mev.atos.net",
    "https://wordpress-sporteurope-tst.mth.mev.atos.net",  
    "https://wordpress-skopje-tst.mth.mev.atos.net",     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)



CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_TOKEN_URL = os.getenv("KEYCLOAK_TOKEN_URL")

logger.info("CLIENT_SECRET %s", CLIENT_SECRET)
logger.info("TOKEN_URL: %s", KEYCLOAK_TOKEN_URL)

@app.post("/token")
async def token(grant_type: str = Form(...),code: str = Form(...),redirect_uri: str = Form(...),client_id: str = Form(...)
):
      
    logger.info("Sending request to %s", KEYCLOAK_TOKEN_URL)
    
    data = {
        "grant_type": grant_type,
        "code": code,
        "client_id": client_id,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": redirect_uri,
    }
    
    response = requests.post(KEYCLOAK_TOKEN_URL, data=data)

    if response.status_code != 200:
      raise HTTPException(status_code=401, detail="Failed to exchange code for token")

    logger.info(" Generated access token: %s",response.json())
    return response.json()
    

   

