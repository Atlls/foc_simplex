const { createApp, ref } = Vue;

createApp({
  setup() {
    // Matriz inicial 2x2
    const A_matrix = ref([
      [0, 0],
      [0, 0]
    ]);
    
    const var_matrix = ref(
      A_matrix.value[0].map( (elm,index) => 'x_'+(index+1))
    )

    const b_matrix = ref(
      A_matrix.value.map( elm => 0 )
    )

    const c_matrix = ref(
      A_matrix.value.map( elm => 0 )
    )


    const addRow = () => {
        const newRow = Array(A_matrix.value[0].length).fill(0);
        A_matrix.value.push(newRow);
        b_matrix.value.push(0);

    };

    const delRow = () => {
        if (A_matrix.value.length > 2)
        {
          A_matrix.value.pop();
          b_matrix.value.pop();
        }
    };

    // Agregar nueva columna
    const addColumn = () => {
      A_matrix.value.forEach(row => row.push(0));
      last_var = A_matrix.value[0].length;
      var_matrix.value.push('x_'+last_var);
      c_matrix.value.push(0);
    };

    const delColumn = () => {
        if (A_matrix.value[0].length > 2)
        {
          A_matrix.value.forEach(row => row.pop());
          var_matrix.value.pop();
          c_matrix.value.pop();
        }
    };

    const convertMatrixToNumbers = (matrix) => {
      return matrix.map(row => {
          return row.map(value => {
              if (typeof value === 'string' && !isNaN(value)) {
                  return parseFloat(value);
              } else if (typeof value !== 'number') {
                  throw new Error(`Invalid value detected in matrix: ${value}`);
              }
              return value;
          });
      });
    };

    const convertListToNumbers = (list) => {
      return list.map(value => {
          if (typeof value === 'string' && !isNaN(value)) {
              return parseFloat(value);
          } else if (typeof value !== 'number') {
              throw new Error(`Invalid value detected in list: ${value}`);
          }
          return value;
      });
    };

    const submitMatrix = async () => {
        try {
            const validatedA = convertMatrixToNumbers(A_matrix.value);
            const validatedb = convertListToNumbers(b_matrix.value);
            const validatedc = convertListToNumbers(c_matrix.value);

            console.log('Validated Matrices:', { validatedA, validatedb, validatedc });

            const response = await fetch('/api/process-data', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                matrix: validatedA,
                firstArray: validatedb,
                secondArray: validatedc,
                varables: var_matrix.value
              })
          });

          const result = await response.json();
          console.log('Resultado:', result);
            
            // Aquí puedes enviar las matrices al endpoint
        } catch (error) {
            console.error('Error in submitMatrix:', error.message);
        }
    };

    return {
      b_matrix,
      A_matrix,
      c_matrix,
      var_matrix,
      addRow,
      delRow,
      addColumn,
      delColumn,
      submitMatrix,
    };
  }
}).mount('#app');