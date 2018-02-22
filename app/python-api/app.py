import numpy as np

import cnn
import cv2
import jsonpickle
from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/predict', methods=['POST'])
def test():
    req = request

    # convert string of image data to uint8
    nparr = np.fromstring(req.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img2 = cv2.resize(img, (224, 224))
    try:
        resp = Response(response=jsonpickle.encode(cnn.dog_classifier(img2)), status=200, mimetype="application/json")
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp
    except:
        resp = Response(response=jsonpickle.encode({'error': 'The image provided does not resemble a human or dog!'}), status=400, mimetype="application/json")
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
