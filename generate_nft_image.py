from PIL import Image, ImageDraw, ImageFont
import textwrap

def place_image_on_template_with_text(image_path, text):
    # Open the template image
    template_path = './/sample_images//nft_template.png'
    template = Image.open(template_path).convert("RGBA")
    
    # Open the image to be placed
    image = Image.open(image_path).convert("RGBA")
    
    # Resize the image to 680x680
    image = image.resize((680, 680))
    
    # Create a new blank image with the same size as the template and RGBA mode
    combined = Image.new("RGBA", template.size)
    
    # Paste the template image onto the blank image
    combined.paste(template, (0, 0))
    
    # Paste the resized image onto the template at the specified coordinates
    combined.paste(image, (46, 42), image)
    
    # Draw the text
    draw = ImageDraw.Draw(combined)
    
    # Define the area where the text will be placed
    box = (66, 722, 696, 865)  # (left, top, right, bottom)
    text_area_width, text_area_height = box[2] - box[0], box[3] - box[1]
    
    # Initialize variables
    font_path = ".//sample_images//COMICSANS.TTF"
    font_size = 70
    wrapped_text = text
    
    # Adjust font size to fit text within the defined box
    while font_size > 10:  # Minimum font size
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = textwrap.fill(text, width=(text_area_width // (font_size // 2)))
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        if text_width <= text_area_width and text_height <= text_area_height:
            break
        
        font_size -= 1
    
    # Calculate the position to center the text
    text_x = box[0] + (text_area_width - text_width) // 2
    text_y = box[1] + (text_area_height - text_height) // 2
    
    # Draw the text on the image
    draw.multiline_text((text_x, text_y), wrapped_text, fill="black", font=font, align="center")
    
    # Save the result
    output_path = image_path[:-4] + "_NFT.png"
    combined.save(output_path)
    return output_path

#image_path = './/sample_images//ai_image_sample.png'
#text = "Sample Event title. Can vary in length from 10 to 400 characters."

#nft_image_path = place_image_on_template_with_text(image_path, text)
