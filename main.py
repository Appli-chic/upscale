from aura_sr import AuraSR
import requests
from io import BytesIO
from PIL import Image
from flask import Flask, request, send_file

app = Flask(__name__)
aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")

def load_image_from_url(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    return Image.open(image_data)

@app.route('/upscale', methods=['GET'])
def upscale():
    # Get the image URL from the request parameters
    image_url = request.args.get('url')

    if not image_url:
        return "Please provide an image URL as a parameter", 400

    try:
        # Load the image from the URL
        image = load_image_from_url(image_url)

        # Upscale the image
        upscaled_image = aura_sr.upscale_4x_overlapped(image)

        # Save the upscaled image to a BytesIO object
        img_io = BytesIO()
        upscaled_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the upscaled image
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
