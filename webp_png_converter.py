from PIL import Image

def convert_webp(webp_file):
    image_name = webp_file[:-5]
    print(image_name)
    webp_image = Image.open(webp_file)

    png_image = webp_image.convert("RGBA")
    png_image.save(image_name + ".png")
    return image_name + ".png"

file_path = ".//sample_images//paris_nft.webp"
png_url = convert_webp(file_path)
print(f"PNG Image: {png_url}")
