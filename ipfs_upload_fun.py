import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    api_key = os.getenv("PINATA_API_KEY")
    api_secret = os.getenv("PINATA_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API Key and Secret must be set in .env file")

    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file}, headers=headers)
    
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        #return f"https://lime-neighbouring-mole-554.mypinata.cloud/ipfs/{ipfs_hash}"
        return f"ipfs://{ipfs_hash}/"
    else:
        raise Exception(f"Error: {response.status_code}, {response.json()}")

# Usage
#file_path = ".//sample_images//ayy_lmao2.jpg"
#ipfs_url = upload_to_pinata(file_path)
#print(f"IPFS URL: {ipfs_url}")
