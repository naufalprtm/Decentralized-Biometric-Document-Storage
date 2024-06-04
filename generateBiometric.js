function generateBiometricHex() {
    console.log("generateBiometricHex function called"); // Debug log
    const hex = generateRandomHex(64); // 64 bytes = 512 bits
    document.getElementById('biometric-auth').value = hex;
    showHexVisualization('hex-visualization', hex);
}

function hexToDescriptor(hex) {
    const descriptor = [];
    for (let i = 0; i < hex.length; i += 4) {
        const chunk = hex.substring(i, i + 4);
        const value = parseInt(chunk, 16) / 65535;
        descriptor.push(value);
    }
    return descriptor;
}

function generateBiometricToken(masks, descriptor) {
    if (!masks || !descriptor) {
        console.error('Invalid input data for token generation');
        return null;
    }

    const token = {}; // Implementasi token sesuai kebutuhan Anda
    return token;
}

function requestMasks(descriptor, forAuth) {
    const encodedDescriptor = encodeDescriptor(descriptor);
    const request = {
        descriptor: encodedDescriptor,
        forAuth: forAuth
    };
    const masks = getMasksFromNodes(request);
    return masks;
}


// Function to generate a random hex string of given size
function generateRandomHex(size) {
    let result = '';
    const characters = '0123456789abcdef';
    for (let i = 0; i < size * 2; i++) {
        result += characters[Math.floor(Math.random() * 16)];
    }
    return result;
}


function getMasksFromNodes() {
    return ['share1', 'share2', 'share3'];
}