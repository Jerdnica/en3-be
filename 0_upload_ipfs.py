#!/usr/bin/env python3

import os
import requests
import re
import textwrap
import json
import sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
from dotenv import load_dotenv
from ai_image_gen import generate_image, download_image_from_url
from generate_nft_image import place_image_on_template_with_text
from ipfs_upload_fun import upload_to_pinata
from generate_nft_metadata import generate_nft_metadata

def main(location, event_name, event_desc, nft_image_path):
    # Load API key from .env file
    load_dotenv()

    chatgpt_API = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=chatgpt_API)

    # Upload NFT to IPFS
    ipfs_url = upload_to_pinata(nft_image_path)
    print(f"IPFS Image URL: {ipfs_url}")

    # Generate NFT Metadata
    nft_metadata_path = generate_nft_metadata(event_name, event_desc, location, nft_image_path, ipfs_url)
    print(f"Metadata File: {nft_metadata_path}")

    # Upload NFT Metadata to IPFS
    ipfs_metadata_url = upload_to_pinata(nft_metadata_path)
    print(f"IPFS Metadata URL: {ipfs_metadata_url}")

    print("ALL DONE!")
    return ipfs_metadata_url

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python upload_nft.py <location> <event_name> <event_desc> <nft_image_path>")
        sys.exit(1)

    location = sys.argv[1]
    event_name = sys.argv[2]
    event_desc = sys.argv[3]
    nft_image_path = sys.argv[4]

    ipfs_metadata_url = main(location, event_name, event_desc, nft_image_path)
    print(ipfs_metadata_url)
