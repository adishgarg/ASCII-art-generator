from flask import Flask, request, redirect, render_template
from PIL import Image
import io

app = Flask(__name__)

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]
    return ascii_str

@app.route('/')
def upload_page():
    return render_template('index.html')

@app.route('/ascii', methods=['POST'])
def generate_ascii():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        image = Image.open(io.BytesIO(file.read()))
        new_image_data = pixels_to_ascii(grayify(resize_image(image)))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join([new_image_data[index:(index+100)] for index in range(0, pixel_count, 100)])
        return render_template('art.html', ascii_art=ascii_image)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
