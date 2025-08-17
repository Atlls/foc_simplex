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

    console.log(b_matrix.value);
    console.log(c_matrix.value);

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

    const submitMatrix = () => {
        console.log("Matriz actualizada:");
        console.table(A_matrix.value);
        
        // Mostrar como objeto JSON formateado
        console.log("Matriz (JSON):", JSON.stringify(A_matrix.value, null, 2));
        
        // Aquí puedes agregar lógica para enviar al backend
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