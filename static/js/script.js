// DOM Elements
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const copyBtn = document.getElementById('copyBtn');
const generateBtn = document.getElementById('generateBtn');
const strengthFill = document.getElementById('strengthFill');
const strengthLabel = document.getElementById('strengthLabel');
const mlPredictionSpan = document.getElementById('mlPrediction');
const entropySpan = document.getElementById('entropy');
const scoreSpan = document.getElementById('score');
const scoreNumber = document.getElementById('scoreNumber');
const breachMessage = document.getElementById('breachMessage');
const recommendationsList = document.getElementById('recommendationsList');
const feedbackContainer = document.getElementById('feedbackContainer');
const lengthStat = document.getElementById('lengthStat');
const uppercaseStat = document.getElementById('uppercaseStat');
const lowercaseStat = document.getElementById('lowercaseStat');
const digitsStat = document.getElementById('digitsStat');
const specialStat = document.getElementById('specialStat');

// Debounce function
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Update UI with analysis results
function updateUI(data) {
    // Update strength meter
    const score = data.score;
    const width = (score / 100) * 100;
    strengthFill.style.width = `${width}%`;
    
    // Set color based on strength
    if (score < 30) {
        strengthFill.style.background = '#ff4444';
        strengthLabel.textContent = 'Very Weak';
    } else if (score < 50) {
        strengthFill.style.background = '#ff8800';
        strengthLabel.textContent = 'Weak';
    } else if (score < 70) {
        strengthFill.style.background = '#ffcc00';
        strengthLabel.textContent = 'Medium';
    } else if (score < 90) {
        strengthFill.style.background = '#44ff44';
        strengthLabel.textContent = 'Strong';
    } else {
        strengthFill.style.background = '#00ffcc';
        strengthLabel.textContent = 'Very Strong';
    }
    
    // Update circular score
    const circumference = 452;
    const offset = circumference - (score / 100) * circumference;
    const scoreCircle = document.querySelector('.score-value');
    if (scoreCircle) {
        scoreCircle.style.strokeDashoffset = offset;
    }
    scoreNumber.textContent = score;
    scoreSpan.textContent = score;
    
    // Update ML prediction
    mlPredictionSpan.textContent = data.ml_prediction || data.strength_text;
    
    // Update entropy
    entropySpan.textContent = `${data.entropy} bits`;
    
    // Update breach status
    if (data.breach_status.breached) {
        breachMessage.innerHTML = `<strong>${data.breach_status.message}</strong>`;
        breachMessage.className = `breach-alert ${data.breach_status.risk_level}`;
    } else {
        breachMessage.innerHTML = `<strong>✅ ${data.breach_status.message}</strong>`;
        breachMessage.className = 'breach-alert none';
    }
    
    // Update recommendations
    recommendationsList.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
    
    // Update character stats
    lengthStat.textContent = data.char_breakdown.length;
    uppercaseStat.textContent = data.char_breakdown.uppercase;
    lowercaseStat.textContent = data.char_breakdown.lowercase;
    digitsStat.textContent = data.char_breakdown.digits;
    specialStat.textContent = data.char_breakdown.special;
    
    // Update feedback items
    updateFeedback(data.checks);
}

// Update live feedback
function updateFeedback(checks) {
    const feedbacks = [
        { key: 'length', text: 'Length (12+ characters)' },
        { key: 'uppercase', text: 'Uppercase letters' },
        { key: 'lowercase', text: 'Lowercase letters' },
        { key: 'digits', text: 'Numbers' },
        { key: 'special', text: 'Special characters' },
        { key: 'entropy', text: 'High randomness' }
    ];
    
    feedbackContainer.innerHTML = '';
    feedbacks.forEach(fb => {
        const div = document.createElement('div');
        div.className = `feedback-item ${checks[fb.key] ? 'valid' : 'invalid'}`;
        div.innerHTML = checks[fb.key] ? `✓ ${fb.text}` : `✗ ${fb.text}`;
        feedbackContainer.appendChild(div);
    });
}

// Analyze password
async function analyzePassword(password) {
    if (!password) {
        resetUI();
        return;
    }
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password })
        });
        
        const data = await response.json();
        if (data.success) {
            updateUI(data);
        } else if (data.error) {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Reset UI when password is empty
function resetUI() {
    strengthFill.style.width = '0%';
    strengthLabel.textContent = 'Enter a password';
    mlPredictionSpan.textContent = '---';
    entropySpan.textContent = '---';
    scoreSpan.textContent = '0';
    scoreNumber.textContent = '0';
    breachMessage.innerHTML = '';
    recommendationsList.innerHTML = '';
    feedbackContainer.innerHTML = '';
    lengthStat.textContent = '0';
    uppercaseStat.textContent = '0';
    lowercaseStat.textContent = '0';
    digitsStat.textContent = '0';
    specialStat.textContent = '0';
}

// Generate strong password
async function generatePassword() {
    try {
        const response = await fetch('/api/generate');
        const data = await response.json();
        passwordInput.value = data.password;
        analyzePassword(data.password);
    } catch (error) {
        console.error('Error generating password:', error);
    }
}

// Copy password to clipboard
function copyPassword() {
    const password = passwordInput.value;
    if (!password) return;
    
    navigator.clipboard.writeText(password).then(() => {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Toggle password visibility
function togglePasswordVisibility() {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    togglePassword.textContent = type === 'password' ? 'Show' : 'Hide';
}

// Initialize particles background
function initParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.insertBefore(canvas, document.body.firstChild);
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    function createParticles() {
        const particleCount = 100;
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 2 + 1,
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                alpha: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(particle => {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(0, 243, 255, ${particle.alpha})`;
            ctx.fill();
            
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            if (particle.x < 0) particle.x = canvas.width;
            if (particle.x > canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = canvas.height;
            if (particle.y > canvas.height) particle.y = 0;
        });
        requestAnimationFrame(drawParticles);
    }
    
    window.addEventListener('resize', () => {
        resizeCanvas();
        particles = [];
        createParticles();
    });
    
    resizeCanvas();
    createParticles();
    drawParticles();
}

// Event listeners
passwordInput.addEventListener('input', debounce((e) => {
    const password = e.target.value;
    analyzePassword(password);
}, 500));

togglePassword.addEventListener('click', togglePasswordVisibility);
copyBtn.addEventListener('click', copyPassword);
generateBtn.addEventListener('click', generatePassword);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    analyzePassword('');
});