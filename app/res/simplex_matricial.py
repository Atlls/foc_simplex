# -*- coding: utf-8 -*-
import polars as pl
import numpy as np

def get_base_matrix(columns, df_A):
    """
    Returns Base and No-Base matrix depends
    of columns param and A matrix.
    Returns (df_base, df_no_base)
    """
    base = []  # Básica.
    no_base = [] # No básica.
    for A_column in df_A.columns:
        value = df_A[A_column]
        if A_column in columns:
            base.append(value)
        else:
            no_base.append(value)

    df_base = pl.DataFrame(base)
    df_no_base = pl.DataFrame(no_base)

    return (df_base, df_no_base)

def get_inverse(df):
    """
    Returns a DataFrame inverted
    """
    npdf = df.to_numpy()
    print(npdf, "-------")
    npdft = np.linalg.inv(npdf)
    dft = pl.DataFrame(npdft)
    return dft

def get_coef_matrix(columns, coef_dict):
    """
    Returns coef matrix depends of columns param
    and coef_dict.
    """
    coef_base = []
    coef_no_base = []
    for column in coef_dict.keys():
        value = coef_dict[column]
        if column in columns:
            coef_base.append((column, value))
        else:
            coef_no_base.append((column, value))

    df_coef_base = pl.DataFrame(
        {col: value for (col, value) in coef_base}
    )
    df_coef_no_base = pl.DataFrame(
        {col: value for (col, value) in coef_no_base}
    )
    return (df_coef_base, df_coef_no_base)

def determinate_matrixial_simplex(
        C_matrix,
        A_matrix,
        b_matrix,
):
    """
    Solución Óptima -> {'code': 0, 'z': float, 'sol': {x_i: float,...}}
    Solución no Factible -> {'code': 1}
    Otra cosa -> {'code': 2} 
    """

    df_C = pl.DataFrame(C_matrix)
    df_A = pl.DataFrame(A_matrix)
    df_b = pl.DataFrame(b_matrix)

    print(df_C)
    print(df_A)
    print(df_b)

    c_values = df_C.row(0, named=True)
    base_0_columns = []  # Básica.
    for col_name_c, value_c in c_values.items():
        if not value_c:
            base_0_columns.append(col_name_c)

    # Inicialización de iteración
    band = 3
    base_columns = base_0_columns
    all_positive = False

    while(band):

        # | Matrices de cálculo
        df_base, df_no_base = get_base_matrix(base_columns, df_A) # Bases
        df_base_inv = get_inverse(df_base) # Invertir base
        df_coef_base, df_coef_no_base = get_coef_matrix(base_columns, c_values) # Coeficientes
        x_base = np.dot(df_base_inv, df_b)

        # | Calculo de conclusión
        x_base = np.dot(df_base_inv, df_b)
        z = np.dot(df_coef_base, x_base)

        # | Cálculos de optimalidad:
        # Obtensión de la variable de entrada.
        _ = np.dot(df_coef_base, df_base_inv)
        _ = np.dot(_, df_no_base)
        res = _ - df_coef_no_base

        all_positive = np.array([d > 0 for d in res]).all()
        if all_positive: # Solución encontrada
            break

        df_res = pl.DataFrame(
            {col: value for (col, value) in zip(df_coef_no_base.columns, res[0])}
        )
        min_column = {col: df_res[col].min() for col in df_res.columns}
        min_value = min(min_column.values())
        in_vector = [col for col, valor in min_column.items() if valor == min_value][0]

        # | Cálculos de factibilidad
        # Obtensión de la variable de salida.
        P_in = df_A[in_vector]
        denominator = np.dot(df_base_inv, P_in)

        all_negative = np.array([d <= 0 for d in denominator]).all()
        if all_negative: # Sol no acotada
            break

        denominator = { tag: value for tag, value in zip(df_base.columns, denominator)}
        numerator = x_base
        to_min = {
            d_tag: n/d_value
            for n,d_value,d_tag in
            zip(numerator, denominator.values(), denominator.keys()) if d_value > 0
        }
        min_per_column = {col: to_min[col] for col in to_min.keys()}
        min_global = min(min_per_column.values())
        out_vector = [col for col, valor in min_per_column.items() if valor == min_global][0]

        # print("Variable de entrada: ", in_vector)
        # print("Variable de salida: ", out_vector)

        # | Reseteo de iteración
        base_columns.remove(out_vector)
        base_columns.append(in_vector)
        # print('\n')

        band -= 1
    
    if not band:
        return {'code': 2}

    if all_positive:
        df_base = pl.DataFrame(
            {col: value for (col, value) in zip(df_base.columns, x_base)}
        )
        z = float(z[0][0])
        return {'code': 0, 'z': z, 'sol': df_base.row(0, named=True)}
    elif all_negative:
        return {'code': 1}

# # Matriz C (1x5)
# C = {
#     "x_1": [5],
#     "x_2": [4],
#     "x_3": [0],
#     "x_4": [0],
#     "x_5": [0],
#     "x_6": [0],
# }

# # Matriz A (4x5)
# A = {
#     "x_1": [6, 1, -1, 0],
#     "x_2": [4, 2, 1, 1],
#     "x_3": [1, 0, 0, 0],
#     "x_4": [0, 1, 0, 0],
#     "x_5": [0, 0, 1, 0],
#     "x_6": [0, 0, 0, 1],
# }

# # Matriz b (1x4)
# b = {
#     "c_1": [24, 6, 1, 2],
# }

# res = determinate_matrixial_simplex(C, A, b)
# print(res)