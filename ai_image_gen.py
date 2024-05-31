import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

chatgpt_API = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=chatgpt_API)

# Function to generate an image using OpenAI's DALL-E API
def generate_image(hex_color, location, event_name, event_desc):
    req_str = "No Text, No characters in image. Accent color should be " + hex_color + ". Make it simple, in minimalistic design. Use landmark from " + location + ". Event is: " + event_name + ". Description (Less relevant): " + event_desc + ". No Text, No characters in image!"

    response = client.images.generate(
        model="dall-e-3",
        prompt=req_str,
        n=1,
        size="1024x1024",
        quality="standard"
    )

    image_url = response.data[0].url
    return image_url

hex_color = "#0078ff"
location = "Belgrade, Serbia"
event_name = "Belgrade ETH Hackathon 2024"
event_desc = "ETH Belgrade Hackathon offers a three-day hacking experience with a primary focus on building on Ethereum. Following the success of the inaugural hackathon in 2023, we aim to surpass it in every aspect. This year, we're opening the doors for builders from all around the globe to join us both in-person and online (hybrid). Our goal is to gather hundreds of hackers and curious minds to develop projects and use cases that will reshape the Ethereum landscape and enhance people's lives."

image_url = generate_image(hex_color, location, event_name, event_desc)
print(f"Generated image URL: {image_url}")
