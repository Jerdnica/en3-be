import os, requests, re, textwrap, json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from openai import OpenAI
from dotenv import load_dotenv

from ai_image_gen import generate_image, download_image_from_url
from generate_nft_image import place_image_on_template_with_text
from ipfs_upload_fun import upload_to_pinata
from generate_nft_metadata import generate_nft_metadata

# Load API key from .env file
load_dotenv()

chatgpt_API = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=chatgpt_API)

# Define inputs
hex_color = "#f4c154"
location = "New York, New York"
event_name = "Beer tasting competition 2024"
event_desc = "The Brewers Association developed the World Beer Cup Competition in 1996 to celebrate the art and science of brewing. Often referred to as The Olympics of Beer Competitions, the World Beer Cup is the most prestigious beer competition in the world."

# Use AI to generate image url
image_url = generate_image(hex_color, location, event_name, event_desc)
print(f"Generated image URL: {image_url}")

# Save AI image to file
image_file = download_image_from_url(image_url, event_name)
print(f"Generated image File: {image_file}")

# Generate NFT from AI image
nft_image_path = place_image_on_template_with_text(image_file, event_name)
print(f"Generated NFT File: {nft_image_path}")

# Upload NFT to IPFS
ipfs_url = upload_to_pinata(nft_image_path)
print(f"IPFS Image URL: {ipfs_url}")

# Generate NFT Metadata
nft_metadata_path = generate_nft_metadata(event_name, event_desc, location, nft_image_path, ipfs_url)
print(f"Metadata File: {nft_metadata_path}")

# Upload NFT to IPFS
ipfs_metadata_url = upload_to_pinata(nft_metadata_path)
print(f"IPFS Metadata URL: {ipfs_metadata_url}")

print("ALL DONE!")