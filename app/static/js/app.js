const { createApp, ref } = Vue;

createApp({
  setup() {
    // Matriz inicial 2x2
    const matrix = ref([
      [0, 0],
      [0, 0]
    ]);

    const addRow = () => {
        const newRow = Array(matrix.value[0].length).fill(0);
        matrix.value.push(newRow);
    };

    const delRow = () => {
        if (matrix.value.length > 2)
            matrix.value.pop();
    };

    // Agregar nueva columna
    const addColumn = () => {
      matrix.value.forEach(row => row.push(0));
    };

    const delColumn = () => {
        if (matrix.value[0].length > 2)
            matrix.value.forEach(row => row.pop());
    };

    const submitMatrix = () => {
        console.log("Matriz actualizada:");
        console.table(matrix.value);
        
        // Mostrar como objeto JSON formateado
        console.log("Matriz (JSON):", JSON.stringify(matrix.value, null, 2));
        
        // Aquí puedes agregar lógica para enviar al backend
    };

    return {
      matrix,
      addRow,
      delRow,
      addColumn,
      delColumn,
      submitMatrix,
    };
  }
}).mount('#app');