const { createApp, ref, onMounted } = Vue;

createApp({
  setup() {
    // Estado reactivo
    const vueMessage = ref('¡Hola Mundo desde Vue 3 Composition API!');
    const randomNumber = ref(null);
    const loading = ref(false);

    const getRandomNumber = async () => {
    loading.value = true;
        try {
            const data = await fetch('/api/random').then(r => r.json());
            randomNumber.value = data.number;
        } catch (err) {
            console.error('Error:', err);
        } finally {
            loading.value = false;
        }
    };

    // Al montar el componente, obtener un número
    onMounted(() => {
      getRandomNumber();
    });

    // Exponer al template
    return {
      vueMessage,
      randomNumber,
      loading,
      getRandomNumber
    };
  }
}).mount('#app');