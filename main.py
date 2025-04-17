from fastapi import FastAPI, Request, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("sso-app")

origins = [
    "http://localhost:8080",  # or whatever your frontend runs on
    "https://wordpress-bakuriani-tst.mth.mev.atos.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# --- CONFIGURE THESE VALUES ---
KEYCLOAK_BASE_URL = "https://keycloak-tst.mth.mev.atos.net"
REALM = "EOC"
CLIENT_ID = "myclient"
CLIENT_SECRET = "mysecret"
REDIRECT_URI = "http://localhost:8000/callback"
# ------------------------------

TOKEN_URL = f"{KEYCLOAK_BASE_URL}/realms/{REALM}/protocol/openid-connect/token"



@app.post("/token")
async def token(grant_type: str = Form(...),code: str = Form(...),redirect_uri: str = Form(...),client_id: str = Form(...)
):
      
    logger.info("Sending request to %s", TOKEN_URL)
    
    data = {
        "grant_type": grant_type,
        "code": code,
        "client_id": client_id,
     #   "client_secret": CLIENT_SECRET,
        "redirect_uri": redirect_uri,
    }
    
    response = requests.post(TOKEN_URL, data=data)

    if response.status_code != 200:
      raise HTTPException(status_code=401, detail="Failed to exchange code for token")

    logger.info(" Generated access token: %s",response.json())
    return response.json()
    

   

