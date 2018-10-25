"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from python_webapp_flask import app
import base64
import os
#from application.python_webapp_flask import image_compare as imag



from io import BytesIO
from skimage.measure import compare_ssim
from skimage.io import imsave
import imutils
import cv2
import numpy
from application.python_webapp_flask.image_compare import compare_images


@app.route('/')
@app.route('/home')
def home():
    compare_images()
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    img.compare_images()
    return render_template(
        'contact.html',
        title='Contact',
        #year=datetime.now().year,
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/upload')
def fileupload():
    return render_template('imagediff.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # calculate and show the image on browser
        calculate_diff(request)

        image_map = {"Original": 'Original.jpg',
                     "Modified": 'Modified.jpg'}

        diff_map = {"Diff": os.path.join(app.config['UPLOAD_FOLDER'], 'Diff.jpg')}

        for name, file_name in image_map.items():
            image_map[name] = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        return render_template("diff.html", images=image_map, diffs=diff_map)


def calculate_diff(request):

    imageA = cv2.imdecode(numpy.fromstring(request.files['firstimage'].read(), numpy.uint8), -1)
    imageB = cv2.imdecode(numpy.fromstring(request.files['secondimage'].read(), numpy.uint8), -1)

    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "Original.jpg"), imageA)
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "Modified.jpg"), imageB)

    # difference = cv2.subtract(imageA, imageB)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # show the output images
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "Diff.jpg"), imageB)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "Actual_Diff.jpg"), diff)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "Thresh.jpg"), thresh)

if __name__ == '__main__':
   app.run(debug=True)
