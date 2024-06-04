function encryptDocumentContent(content, hexKey) {
    const key = CryptoJS.enc.Hex.parse(hexKey);
    const iv = CryptoJS.lib.WordArray.random(128 / 8);
    const encrypted = CryptoJS.AES.encrypt(content, key, {
        mode: CryptoJS.mode.CBC,
        iv: iv,
        padding: CryptoJS.pad.Pkcs7
    });
    return iv.toString() + encrypted.toString();
}
function encryptDocument(button) {
    const documentItem = button.parentElement;
    const documentContent = documentItem.dataset.documentContent;
    const hexKey = document.getElementById('biometric-auth').value;
    const encryptedContent = encryptDocumentContent(documentContent, hexKey);
    documentItem.dataset.encryptedContent = encryptedContent;
    documentItem.dataset.documentContent = '';
    showEncryptionVisualization('encryption-visualization');
    showHexVisualization('encryption-visualization', hexKey);
    const publicShareHash = calculatePublicShareHash(encryptedContent);
    document.getElementById('public-share-hash').value = publicShareHash;
}
function calculatePublicShareHash(encryptedContent) {
    return CryptoJS.SHA256(encryptedContent).toString();
}
// Function to decrypt a document
function decryptDocument() {
    const hexKey = document.getElementById('decrypt-key').value;
    console.log('Hex Key:', hexKey);  // Debug log
    const documentList = document.getElementById('documents-list');
    const documentItems = documentList.getElementsByClassName('document-item');

    if (documentItems.length > 0) {
        const documentItem = documentItems[0];
        const encryptedContent = documentItem.dataset.encryptedContent;
        console.log('Encrypted Content:', encryptedContent);  // Debug log

        checkBiometricTokenValidity(hexKey)
            .then(response => {
                console.log('Token Validity Response:', response);  // Debug log
                if (response.valid) {
                    const decryptedContent = decryptContent(encryptedContent, hexKey);
                    document.getElementById('decrypted-content').value = decryptedContent;
                    showHexVisualization('decryption-visualization', hexKey);
                } else {
                    alert('Biometric token has expired. Please generate a new token.');
                }
            })
            .catch(error => {
                console.error('Error checking biometric token validity:', error);
                alert('An error occurred while checking biometric token validity.');
            });
    }
}


function decryptContent(encryptedContent, hexKey) {
    const key = CryptoJS.enc.Hex.parse(hexKey);
    const iv = CryptoJS.enc.Hex.parse(encryptedContent.slice(0, 32));
    const encrypted = encryptedContent.slice(32);
    const decrypted = CryptoJS.AES.decrypt(encrypted, key, {
        mode: CryptoJS.mode.CBC,
        iv: iv,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}