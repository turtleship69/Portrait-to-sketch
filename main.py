import cv2
from flask import Flask, render_template, send_file, request, redirect
from os import urandom
import numpy as np
from io import BytesIO


def sketcher(input):
    img = get_opencv_img_from_buffer(input, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image
    blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    inverted_blurred_img = 255 - blurred_img
    pencil_sketch_IMG = cv2.divide(gray_image,
                                   inverted_blurred_img,
                                   scale=256.0)
    #source: https://python.plainenglish.io/convert-a-photo-to-pencil-sketch-using-python-in-12-lines-of-code-4346426256d4e
    return pencil_sketch_IMG

def get_opencv_img_from_buffer(buffer, flags):
    bytes_as_np_array = np.frombuffer(buffer.read(), dtype=np.uint8)
    return cv2.imdecode(bytes_as_np_array, flags)

#generate random alphanumerical string 
def random_string(length):
    return urandom(length).hex()

app = Flask(__name__)
app.secret_key = urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sketch', methods=['GET', 'POST'])
def sketch():
    """take picture from post request, convert to sketch and return file in png form with mine types"""
    if request.method == 'POST':
        #convert image to sketch from request.files['image']
        sketched_image = sketcher(request.files['image'].stream)
        #convert sketch to image that can be returned to browser
        sketched_image = cv2.imencode('.png', sketched_image)[1].tostring()
        #return sketch to browser
        return send_file(BytesIO(sketched_image), mimetype='image/png')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)