function deleteDocument(button) {
    const documentItem = button.parentElement;
    console.log('Deleting document:', documentItem); // Debug log
    documentItem.remove();
    alert('Document deleted!');

    // Kosongkan gambar visualisasi dan hasil hash
    document.getElementById('encryption-visualization').innerHTML = '';
    console.log('Cleared encryption visualization'); // Debug log

    document.getElementById('public-share-hash').value = '';
    console.log('Cleared public share hash'); // Debug log

    const nodeSharesVisualization = document.getElementById('node-shares-visualization');
    if (nodeSharesVisualization) {
        const nodeSharesContainer = nodeSharesVisualization.querySelector('.node-share-container');
        if (nodeSharesContainer) {
            // Lanjutkan dengan logika Anda di sini
        } else {
            console.error("Element with class 'node-share-container' not found inside 'node-shares-visualization'.");
        }
    } else {
        console.error("Element with ID 'node-shares-visualization' not found.");
    }
    
    document.getElementById('view-visualization').innerHTML = '';
    console.log('Cleared view visualization'); // Debug log

    // Kosongkan visualisasi dan bar dekripsi
    document.getElementById('decryption-visualization').innerHTML = '';
    console.log('Cleared decryption visualization'); // Debug log

    document.getElementById('decrypted-content').value = '';
    console.log('Cleared decrypted content'); // Debug log

    document.getElementById('upload-visualization').innerHTML = '';
    console.log('Cleared upload visualization'); // Debug log

    // Hapus semua SVG yang dihasilkan
    const generatedSVGContainers = document.querySelectorAll('.svg-container');
    generatedSVGContainers.forEach(container => {
        container.remove();
    });
}
