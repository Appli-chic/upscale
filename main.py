from aura_sr import AuraSR
from io import BytesIO
from PIL import Image
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")

@app.route('/upscale', methods=['POST'])
def upscale():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "Please provide an image file in the request", 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return "No selected file", 400

    try:
        # Load the image from the uploaded file
        image = Image.open(file.stream)

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
    app.run(host='0.0.0.0', port=5000)
