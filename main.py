from aura_sr import AuraSR
import requests
from io import BytesIO
from PIL import Image

aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")

def load_image_from_url(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    return Image.open(image_data)

image = load_image_from_url("https://www.happybrainscience.com/wp-content/uploads/2017/07/derwent-morning-Cropped.jpg")
upscaled_image = aura_sr.upscale_4x_overlapped(image)

upscaled_image.save("upscaled_image.png")
