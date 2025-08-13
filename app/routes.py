from app import app
from flask import render_template, jsonify
import random

@app.route('/')
def home():
    return render_template('index.html', message="Flask + Vue.js Integration")

@app.route('/api/random')
def random_number():
    return jsonify({'number': random.randint(1, 100)})