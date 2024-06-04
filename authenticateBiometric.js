// Fungsi untuk mengirim permintaan autentikasi biometrik ke server
function authenticateBiometric(hex) {
    fetch('/authenticate-biometric', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hex_key: hex }) // Mengirim hex key dalam format JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.authenticated) {
            alert('Biometric authenticated successfully!');
        } else {
            alert('Biometric authentication failed!');
        }
    })
    .catch(error => {
        console.error('Error authenticating biometric:', error);
        alert('An error occurred while authenticating biometric.');
    })
    .finally(() => {
        document.getElementById('biometric-auth').value = '';
    });
};


// Function to update biometric token on the server
function updateBiometricToken(hex) {
    console.log("Updating biometric token with hex:", hex);
    fetch('/update-biometric-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hex_key: hex }) // Sending hex key in JSON format
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Biometric token updated successfully!');
        } else {
            console.error('Failed to update biometric token:', data.error);
        }
    })
    .catch(error => {
        console.error('Error updating biometric token:', error);
    });
}


function checkBiometricTokenValidity(hexKey) {
    // Menghitung waktu token expired dalam waktu 5 menit dari sekarang
    const expiryTime = new Date();
    expiryTime.setMinutes(expiryTime.getMinutes() + 5);

    return fetch('/validate-biometric-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            hex_key: hexKey,
            expiry_time: expiryTime.toISOString() // Mengirim waktu kedaluwarsa dalam format ISO string
        })  
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.valid) {
            console.log('Biometric token is valid.');
        } else {
            console.log('Biometric token has expired.');
        }
        return data.valid;
    })
    .catch(error => {
        console.error('Error checking biometric token validity:', error);
        throw error;
    });
}


