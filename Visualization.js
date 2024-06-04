// Fungsi untuk menghasilkan pola kubus berdasarkan hex key
function generateCubePattern(rows, cols, hexKey) {
    let pattern = '';
    const colors = ['#000', '#fff', '#ccc'];
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const index = (i * cols + j) % hexKey.length;
            const colorIndex = parseInt(hexKey.charAt((i * cols + j) % hexKey.length), 16) % colors.length;
            const color = colors[colorIndex];
            pattern += `<rect x="${j * 30}" y="${i * 30}" width="30" height="30" fill="${color}" />`;
        }
    }
    return pattern;
}
function showHexVisualization(elementId, hexKey) {
    const svgElement = `
        <svg width="200" height="200">
            ${generateCubePattern(6, 6, hexKey)}
        </svg>
    `;
    document.getElementById(elementId).innerHTML = svgElement;
}
function showEncryptionVisualization(visualizationId) {
    const encryptionVisualization = document.getElementById(visualizationId);
    const svgElement = `
        <svg width="200" height="200">
            <!-- SVG content for encryption visualization -->
        </svg>
    `;
    encryptionVisualization.innerHTML = svgElement;
}
// Function to generate SVG for shares
function generateSharesSVG() {
    // Placeholder function, replace with actual SVG generation logic
    const svgContent = `
        <circle cx="100" cy="100" r="80" fill="rgba(255, 0, 0, 0.5)" />
        <rect x="40" y="40" width="120" height="120" fill="rgba(0, 255, 0, 0.5)" />
        <polygon points="20,80 50,20 80,80" fill="rgba(0, 0, 255, 0.5)" />
        <circle cx="50" cy="150" r="30" fill="rgba(255, 255, 0, 0.5)" />
        <rect x="100" y="120" width="80" height="60" fill="rgba(255, 0, 255, 0.5)" />
        <polygon points="150,150 180,200 120,200" fill="rgba(0, 255, 255, 0.5)" />
    `;
    return svgContent;
}
// Function to visualize shares
function visualizeShares(shares) {
    const visualizationElement = document.getElementById('node-shares-visualization');
    if (!visualizationElement) {
        console.error("Element with ID 'node-shares-visualization' not found.");
        return;
    }

    const shareContainer = visualizationElement.querySelector('.node-share-container');
    if (!shareContainer) {
        console.error("Element with class 'node-share-container' not found inside 'node-shares-visualization'.");
        return;
    }

    shareContainer.innerHTML = '';
    shares.forEach((share, index) => {
        const nodeShare = document.createElement('div');
        nodeShare.className = 'node-share';
        nodeShare.textContent = `Node ${index + 1}: ${share}`;
        shareContainer.appendChild(nodeShare);
    });

    const svgElement = document.createElement('div');
    svgElement.className = 'svg-container';
    svgElement.innerHTML = `
        <svg id="node-shares-svg" width="200" height="200">
            ${generateSharesSVG()}
        </svg>
    `;
    shareContainer.appendChild(svgElement);
}
