// ============================================
// Configuration
// ============================================

const API_BASE_URL = 'http://localhost:5000';
const FLOWER_SPECIES = {
    'Setosa': '🌸',
    'Versicolor': '🌺',
    'Virginica': '🌼'
};

// ============================================
// DOM Elements
// ============================================

const form = document.getElementById('predictionForm');
const resultCard = document.getElementById('resultCard');
const submitButton = form.querySelector('.submit-button');
const buttonText = submitButton.querySelector('.button-text');
const buttonLoader = submitButton.querySelector('.button-loader');

// ============================================
// Event Listeners
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    form.addEventListener('submit', handlePrediction);
    setupNavigation();
});

// ============================================
// Navigation Setup
// ============================================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// ============================================
// Main Prediction Handler
// ============================================

async function handlePrediction(e) {
    e.preventDefault();
    
    // Validate inputs
    if (!validateInputs()) {
        showError('Please fill in all fields with valid numbers');
        return;
    }
    
    // Get form values
    const formData = {
        sepal_length: parseFloat(document.getElementById('sepalLength').value),
        sepal_width: parseFloat(document.getElementById('sepalWidth').value),
        petal_length: parseFloat(document.getElementById('petalLength').value),
        petal_width: parseFloat(document.getElementById('petalWidth').value)
    };
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayResult(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to get prediction. Make sure the backend server is running on http://localhost:5000');
    } finally {
        setLoadingState(false);
    }
}

// ============================================
// Input Validation
// ============================================

function validateInputs() {
    const sepalLength = parseFloat(document.getElementById('sepalLength').value);
    const sepalWidth = parseFloat(document.getElementById('sepalWidth').value);
    const petalLength = parseFloat(document.getElementById('petalLength').value);
    const petalWidth = parseFloat(document.getElementById('petalWidth').value);
    
    return !isNaN(sepalLength) && !isNaN(sepalWidth) && 
           !isNaN(petalLength) && !isNaN(petalWidth) &&
           sepalLength > 0 && sepalWidth > 0 && 
           petalLength > 0 && petalWidth > 0;
}

// ============================================
// Loading State Management
// ============================================

function setLoadingState(isLoading) {
    submitButton.disabled = isLoading;
    
    if (isLoading) {
        buttonText.classList.add('hidden');
        buttonLoader.classList.remove('hidden');
    } else {
        buttonText.classList.remove('hidden');
        buttonLoader.classList.add('hidden');
    }
}

// ============================================
// Result Display
// ============================================

function displayResult(data) {
    const speciesName = data.prediction;
    const confidence = Math.round(data.confidence * 100);
    const icon = FLOWER_SPECIES[speciesName] || '🌻';
    
    // Update result card
    document.getElementById('speciesName').textContent = speciesName;
    document.getElementById('flowerIcon').textContent = icon;
    document.getElementById('confidenceScore').textContent = confidence;
    
    // Animate confidence bar
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.width = '0%';
    setTimeout(() => {
        confidenceFill.style.width = confidence + '%';
    }, 100);
    
    // Display prediction details
    displayPredictionDetails(data);
    
    // Show result card
    resultCard.classList.remove('hidden');
    
    // Scroll to result
    setTimeout(() => {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

// ============================================
// Prediction Details
// ============================================

function displayPredictionDetails(data) {
    const detailsDiv = document.getElementById('predictionDetails');
    
    const speciesInfo = {
        'Setosa': {
            description: 'Iris Setosa is the smallest of the three species, typically found in coastal areas of eastern North America.',
            characteristics: 'Small sepals and petals, usually grows 25-38 cm tall'
        },
        'Versicolor': {
            description: 'Iris Versicolor is a medium-sized species found in wetland areas across eastern North America.',
            characteristics: 'Medium-sized flowers, typically grows 50-80 cm tall'
        },
        'Virginica': {
            description: 'Iris Virginica is the largest species, native to southeastern United States.',
            characteristics: 'Large flowers with long sepals and petals, grows up to 100+ cm'
        }
    };
    
    const species = data.prediction;
    const info = speciesInfo[species] || {};
    
    let html = `
        <div>
            <p><strong>🔍 About this species:</strong></p>
            <p>${info.description || 'A beautiful iris flower species.'}</p>
            <p style="margin-top: 12px;"><strong>📊 Characteristics:</strong></p>
            <p>${info.characteristics || 'A unique member of the iris family.'}</p>
            <p style="margin-top: 12px;"><strong>📈 Confidence Metrics:</strong></p>
            <p>Model Confidence: <strong>${Math.round(data.confidence * 100)}%</strong></p>
        </div>
    `;
    
    detailsDiv.innerHTML = html;
}

// ============================================
// Error Handling
// ============================================

function showError(message) {
    // Create error notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
        font-weight: 500;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ============================================
// Result Management
// ============================================

function closeResult() {
    resultCard.classList.add('hidden');
}

// ============================================
// Animations (CSS)
// ============================================

// Add animation styles dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .hidden {
        display: none !important;
    }
`;
document.head.appendChild(style);

// ============================================
// Example Data (for testing without backend)
// ============================================

function getExamplePrediction() {
    return {
        prediction: 'Setosa',
        confidence: 0.98
    };
}

// Log API status
console.log(`%c🚀 ML Predictor Started`, 'color: #6366f1; font-size: 14px; font-weight: bold;');
console.log(`%cAPI Base URL: ${API_BASE_URL}`, 'color: #06b6d4; font-size: 12px;');
