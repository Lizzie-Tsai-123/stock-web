# -*- coding: UTF-8 -*-
import app.model as model
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/test')
def index():
    return 'hello test!!'

@app.route('/new', methods = ['POST'])
def postInput():
    #取得前端傳過來的數值
    insert = request.get_json()
    #print(insertValues)
    x1 = insert["d"]
    x2 = insert["stock"]

    inputs = np.array([[x1, x2]])
    functions.pullData(inputs)
    result = functions.drawGraph_s(inputs)
    #print(inputs)
    return jsonify({'return':result})
