import os, requests, re, textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from openai import OpenAI
from dotenv import load_dotenv

from ai_image_gen import generate_image, download_image_from_url
from generate_nft_image import place_image_on_template_with_text
from ipfs_upload_fun import upload_to_pinata

# Load API key from .env file
load_dotenv()

chatgpt_API = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=chatgpt_API)

# Define inputs
hex_color = "#0078ff"
location = "Belgrade, Serbia"
event_name = "Belgrade ETH Hackathon 2026"
event_desc = "ETH Belgrade Hackathon offers a three-day hacking experience with a primary focus on building on Ethereum. Following the success of the inaugural hackathon in 2023, we aim to surpass it in every aspect. This year, we're opening the doors for builders from all around the globe to join us both in-person and online (hybrid). Our goal is to gather hundreds of hackers and curious minds to develop projects and use cases that will reshape the Ethereum landscape and enhance people's lives."

# Use AI to generate image url
image_url = generate_image(hex_color, location, event_name, event_desc)
print(f"Generated image URL: {image_url}")

# Save AI image to file
image_file = download_image_from_url(image_url, event_name)
print(f"Generated image File: {image_file}")

# Generate NFT from AI image
nft_image_path = place_image_on_template_with_text(image_file, event_name)
print(f"Generated NFT File: {nft_image_path}")

# Upload to IPFS
ipfs_url = upload_to_pinata(nft_image_path)
print(f"IPFS URL: {ipfs_url}")
