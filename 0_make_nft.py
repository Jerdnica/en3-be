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

def main(hex_color, location, event_name, event_desc, output_path='nft_image.png'):
    # Load API key from .env file
    load_dotenv()

    chatgpt_API = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=chatgpt_API)

    # Use AI to generate image URL
    image_url = generate_image(hex_color, location, event_name, event_desc)
    print(f"Generated image URL: {image_url}")

    # Save AI image to file
    image_file = download_image_from_url(image_url, event_name)
    print(f"Generated image File: {image_file}")

    # Generate NFT from AI image
    nft_image_path = place_image_on_template_with_text(image_file, event_name)
    print(f"Generated NFT File: {nft_image_path}")

    # Save the final NFT image to the specified output path
    os.rename(nft_image_path, output_path)
    print(f"NFT image saved to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python script.py <hex_color> <location> <event_name> <event_desc> <output_path>")
        sys.exit(1)
    
    hex_color = sys.argv[1]
    location = sys.argv[2]
    event_name = sys.argv[3]
    event_desc = sys.argv[4]
    output_path = sys.argv[5]
    
    main(hex_color, location, event_name, event_desc, output_path)
