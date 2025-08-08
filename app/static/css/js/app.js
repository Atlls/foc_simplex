// Ejemplo de llamada a la API
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('data-container');
        data.data.forEach(item => {
            const p = document.createElement('p');
            p.textContent = `Item: ${item}`;
            container.appendChild(p);
        });
    })
    .catch(error => console.error('Error:', error));