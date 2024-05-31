import requests

def upload_to_pinata(file_path, api_key, api_secret):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file}, headers=headers)
    
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://ipfs.io/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"Error: {response.status_code}, {response.json()}")

# Usage
api_key = "asd"
api_secret = "asd"
file_path = ".//sample_images//ayy_lmao.jpg"

ipfs_url = upload_to_pinata(file_path, api_key, api_secret)
print(f"IPFS URL: {ipfs_url}")