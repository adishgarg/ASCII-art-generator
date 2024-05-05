from flask import Flask, render_template, request
import PIL.Image

app = Flask(__name__)

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height/width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)

def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)
    
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)    
    
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/ascii', methods=['POST'])
def ascii():
    if request.method == 'POST':
        f = request.files['image']
        f.save(f.filename)
        path = f.filename
        image = PIL.Image.open(path)
        new_image_data = pixels_to_ascii(grayify(resize_image(image)))
        pixel_count = len(new_image_data)  
        ascii_image = "\n".join([new_image_data[index:(index+100)] for index in range(0, pixel_count, 100)])
        return ascii_image

if __name__ == '__main__':
    app.run(debug=True)

