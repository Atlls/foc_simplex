from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html', title='Inicio')

@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')

@app.route('/api/data')
def get_data():
    return {'data': [1, 2, 3, 4, 5]}