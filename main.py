import cv2, uuid
from flask import Flask, render_template, send_file, request, redirect, session
from os import urandom, path, remove, listdir

dir = 'content'
for f in listdir(dir):
    remove(path.join(dir, f))
#create empty .gitkeep file to prevent empty folder from being pushed to github
with open('content/.gitkeep', 'w') as f:
    f.write('')


def sketcher(input):
    img = cv2.imread(input)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image
    blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    inverted_blurred_img = 255 - blurred_img
    pencil_sketch_IMG = cv2.divide(gray_image,
                                   inverted_blurred_img,
                                   scale=256.0)
    returnencil_sketch_IMG


app = Flask(__nam
    #source: https://python.plainenglish.io/convert-a-photo-to-pencil-sketch-using-python-in-12-lines-of-code-4346426256d4e__)
app.secret_key = urandom(24)


@app.route('/')
def index():
    """assign a random session id to the user"""
    session['id'] = uuid.uuid4()
    return render_template('index.html')


@app.route('/sketch', methods=['GET', 'POST'])
def sketch():
    """take picture from post request, convert to sketch and return file in png form with mine types"""
    if request.method == 'POST':
        #save session id to variable
        id = random_string(24)
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
