"""
The flask application package.
"""

from flask import Flask
from os import environ
from applicationinsights.requests import WSGIApplication
app = Flask(__name__)
app.wsgi_app = WSGIApplication(environ.get('APPINSIGHTS_INSTRUMENTATIONKEY'), app.wsgi_app)
import python_webapp_flask.views
#code below added by Rajiv
#import base64
#import os
#from io import BytesIO
#from skimage.measure import compare_ssim
#from skimage.io import imsave
#import cv2
#import imutils
#import numpy
#from werkzeug.utils import secure_filename
#import requests
#from PIL import Image
#optional code added by Rajiv below
#import matplotlib.pyplot as plt
#from matplotlib import patches
#UPLOAD_PATH = os.path.join('static','images')
#
#app.config['UPLOAD_FOLDER'] = UPLOAD_PATH




