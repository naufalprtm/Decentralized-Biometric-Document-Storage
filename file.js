function uploadDocument() {
    const fileInput = document.getElementById('document-upload');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const documentContent = e.target.result;
            addDocumentToList(file.name, documentContent);
            visualizeShares(getMasksFromNodes());
        };
        reader.readAsText(file);
    }
}
// Function to add a document to the list
function addDocumentToList(name, documentContent) {
    const documentList = document.getElementById('documents-list');
    const documentItem = document.createElement('div');
    documentItem.className = 'document-item';
    documentItem.dataset.documentContent = documentContent;
    documentItem.innerHTML = `
        <span>${name}</span>
        <button onclick="viewDocument(this)">View</button>
        <button onclick="encryptDocument(this)">Encrypt</button>
        <button onclick="deleteDocument(this)">Delete</button>
    `;
    documentList.appendChild(documentItem);
}
function viewDocument(button) {
    const documentItem = button.parentElement;
    const documentContent = documentItem.dataset.documentContent || documentItem.dataset.encryptedContent;
    alert('Document Content: ' + documentContent);
    showHexVisualization('view-visualization', document.getElementById('biometric-auth').value);
}