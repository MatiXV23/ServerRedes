const ImgBtn = document.getElementById('changeImageBtn');
const img = document.getElementById('mainImage');
const textViewer = document.getElementById('textViewer');
const closeBtn = document.getElementById('closeConn');


ImgBtn.addEventListener('click', async function() {
    console.log('Botón clickeado');
    try {
        const response = await fetch('http://localhost:8082/foto');
        
        if (!response.ok) {
            throw new Error('Error en la petición: ' + response.status);
        }
        console.log(response)

        const data = await response.json();

        console.log(data.data)
    
        const imageUrl = data.data;
        
        textViewer.innerHTML = "Escuchando...";
        img.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
    }
});


closeBtn.addEventListener('click', async function() {
    console.log('Botón clickeado');
    try {
        const response = await fetch('http://localhost:8082/close');
        
        if (!response.ok) {
            throw new Error('Error en la petición: ' + response.status);
        }
        console.log(response)

        const data = await response.json();

        console.log(data.data)
    
        const msg = data.data;
        
        textViewer.innerHTML = msg;
        
    } catch (error) {
        console.error('Error:', error);
    }
});




 