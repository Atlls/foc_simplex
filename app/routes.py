from app import app
from flask import render_template, jsonify, request
from app.res.simplex_matricial import determinate_matrixial_simplex
import random
import polars as pl

@app.route('/')
def home():
    return render_template('index.html', message="Flask + Vue.js Integration")

@app.route('/api/process-data', methods=['POST'])
def process_data():
    data = request.json
    A_matrix_raw = data.get('matrix')
    b_matrix_raw = data.get('firstArray')
    c_matrix_raw = data.get('secondArray')
    variable_raw = data.get('varables')

    # Aquí puedes procesar los datos recibidos
    # print('Datos recibidos:', A_matrix_raw, b_matrix_raw, c_matrix_raw, variable_raw)
    A_matrix_raw = pl.DataFrame(A_matrix_raw).to_numpy()

    A_matrix = {i: row for i, row in zip(variable_raw, A_matrix_raw)}
    c_matrix = {i: [value] for i, value in zip(variable_raw, c_matrix_raw)}
    b_matrix = {'c_1': b_matrix_raw}
    print(A_matrix, b_matrix, c_matrix)
    print()
    d = determinate_matrixial_simplex(c_matrix, A_matrix, b_matrix)
    print(d)
    return jsonify(d)