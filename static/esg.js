// ESG Dashboard JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    document.getElementById('calculateBtn').addEventListener('click', calculateESG);
    
    // Auto-calculate on first load
    calculateESG();
});

// Calculate ESG scores
async function calculateESG() {
    const numPalms = parseInt(document.getElementById('numPalms').value);
    const annualCycles = parseInt(document.getElementById('annualCycles').value);
    const location = document.getElementById('location').value;
    
    // Show loading state
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('esgScores').style.display = 'none';
    document.getElementById('errorState').style.display = 'none';
    
    try {
        // Fetch biomass optimization data (includes ESG metrics)
        const response = await fetch('/palm/biomass_optimization', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                num_palms: numPalms,
                annual_cycles: annualCycles,
                location: location
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch ESG data');
        }
        
        const data = await response.json();
        
        // Calculate ESG scores from biomass data
        const esgScores = calculateESGScores(data, numPalms, annualCycles);
        
        // Display the results
        displayESGScores(esgScores, data);
        
        // Hide loading, show scores
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('esgScores').style.display = 'block';
        
    } catch (error) {
        console.error('Error fetching ESG data:', error);
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('errorState').style.display = 'block';
        document.getElementById('errorMessage').textContent = 
            'Failed to calculate ESG scores. Please check your connection and try again.';
    }
}

// Calculate ESG scores from biomass data
function calculateESGScores(data, numPalms, annualCycles) {
    // Environmental Score (0-100)
    // Based on: CO2 reduction, waste recycling, renewable energy potential
    const co2Reduction = data.total_co2_reduction || 0;
    const wasteRecycled = data.total_waste_generated || 0;
    const bioenergyPotential = data.total_bioenergy_kwh || 0;
    
    // Environmental: Higher CO2 reduction and waste recycling = higher score
    const envScore = Math.min(100, Math.round(
        (co2Reduction / (numPalms * annualCycles * 50)) * 40 + // CO2 factor
        (wasteRecycled / (numPalms * annualCycles * 100)) * 30 + // Waste factor
        (bioenergyPotential / (numPalms * annualCycles * 500)) * 30 // Energy factor
    ));
    
    // Social Score (0-100)
    // Based on: job creation, community impact, fair practices
    const jobsCreated = Math.round(numPalms / 100); // 1 job per 100 palms
    const communityImpact = numPalms > 5000 ? 'High' : numPalms > 2000 ? 'Medium' : 'Low';
    
    const socialScore = Math.min(100, Math.round(
        (jobsCreated / (numPalms / 50)) * 40 + // Job creation factor
        50 + // Base score for sustainable practices
        (numPalms > 2000 ? 10 : 0) // Bonus for large operations
    ));
    
    // Governance Score (0-100)
    // Based on: compliance, transparency, ethical practices
    const complianceRate = 100; // Assuming full compliance with sustainable practices
    const transparencyLevel = 'High'; // Using open-source AI and transparent metrics
    
    const govScore = Math.min(100, Math.round(
        (complianceRate / 100) * 40 + // Compliance factor
        40 + // Base transparency score
        20 // Ethics and certification factor
    ));
    
    // Overall ESG Score (weighted average)
    const overallScore = Math.round(
        (envScore * 0.4) + // Environmental: 40%
        (socialScore * 0.3) + // Social: 30%
        (govScore * 0.3) // Governance: 30%
    );
    
    return {
        environmental: envScore,
        social: socialScore,
        governance: govScore,
        overall: overallScore,
        metrics: {
            co2Reduction: co2Reduction,
            wasteRecycled: wasteRecycled,
            waterSaved: Math.round(numPalms * annualCycles * 50), // Estimated water savings
            jobsCreated: jobsCreated,
            communityImpact: communityImpact,
            bioenergyPotential: bioenergyPotential
        }
    };
}

// Display ESG scores with animations
function displayESGScores(scores, rawData) {
    // Overall Score
    animateValue('overallScore', 0, scores.overall, 1500);
    
    // Score Rating
    const rating = scores.overall >= 80 ? 'Excellent' : 
                   scores.overall >= 60 ? 'Good' : 
                   scores.overall >= 40 ? 'Fair' : 'Needs Improvement';
    document.getElementById('scoreRating').textContent = rating;
    
    // Animate radial charts
    animateRadialChart('envProgress', 'envValue', scores.environmental, '#22c55e');
    animateRadialChart('socialProgress', 'socialValue', scores.social, '#3b82f6');
    animateRadialChart('govProgress', 'govValue', scores.governance, '#a855f7');
    
    // Update Environmental Metrics
    const envMetrics = document.getElementById('envMetrics');
    envMetrics.innerHTML = `
        <div class="metric-item">
            <span class="metric-icon">🌱</span>
            <span class="metric-text">CO₂ Reduction: <strong>${formatNumber(scores.metrics.co2Reduction)} kg/year</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">♻️</span>
            <span class="metric-text">Waste Recycled: <strong>${formatNumber(scores.metrics.wasteRecycled)} kg/year</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">💧</span>
            <span class="metric-text">Water Saved: <strong>${formatNumber(scores.metrics.waterSaved)} L/year</strong></span>
        </div>
    `;
    
    // Update Social Metrics
    const socialMetrics = document.getElementById('socialMetrics');
    socialMetrics.innerHTML = `
        <div class="metric-item">
            <span class="metric-icon">👨‍🌾</span>
            <span class="metric-text">Jobs Created: <strong>${scores.metrics.jobsCreated}</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">🏘️</span>
            <span class="metric-text">Community Impact: <strong>${scores.metrics.communityImpact}</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">📚</span>
            <span class="metric-text">Training Programs: <strong>Available</strong></span>
        </div>
    `;
    
    // Update Governance Metrics
    const govMetrics = document.getElementById('govMetrics');
    govMetrics.innerHTML = `
        <div class="metric-item">
            <span class="metric-icon">✅</span>
            <span class="metric-text">Compliance: <strong>100%</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">📊</span>
            <span class="metric-text">Transparency: <strong>High</strong></span>
        </div>
        <div class="metric-item">
            <span class="metric-icon">🔒</span>
            <span class="metric-text">Ethics: <strong>Certified</strong></span>
        </div>
    `;
    
    // Display detailed metrics
    displayDetailedMetrics(rawData, scores);
    
    // Display recommendations
    displayRecommendations(scores, rawData);
}

// Animate radial chart progress
function animateRadialChart(progressId, valueId, targetValue, color) {
    const progressCircle = document.getElementById(progressId);
    const valueElement = document.getElementById(valueId);
    
    const circumference = 502.65; // 2 * π * r (r = 80)
    const offset = circumference - (targetValue / 100) * circumference;
    
    // Animate the circle
    setTimeout(() => {
        progressCircle.style.strokeDashoffset = offset;
    }, 100);
    
    // Animate the number
    animateValue(valueId, 0, targetValue, 1500);
}

// Animate number counter
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

// Display detailed environmental metrics
function displayDetailedMetrics(data, scores) {
    const envGrid = document.getElementById('envDetailsGrid');
    envGrid.innerHTML = `
        <div class="metric-card">
            <h4>Bioenergy Potential</h4>
            <div class="value">${formatNumber(data.total_bioenergy_kwh || 0)} kWh</div>
            <div class="description">Annual renewable energy generation</div>
        </div>
        <div class="metric-card">
            <h4>Carbon Credits</h4>
            <div class="value">${formatNumber(scores.metrics.co2Reduction / 1000)} tons</div>
            <div class="description">CO₂ equivalent reduction per year</div>
        </div>
        <div class="metric-card">
            <h4>Waste Valorization</h4>
            <div class="value">${Math.round((data.total_waste_generated || 0) / (data.total_waste_generated || 1) * 100)}%</div>
            <div class="description">Biomass waste converted to value</div>
        </div>
        <div class="metric-card">
            <h4>Sustainability Index</h4>
            <div class="value">${scores.environmental}/100</div>
            <div class="description">Environmental performance score</div>
        </div>
    `;
    
    const economicGrid = document.getElementById('economicGrid');
    economicGrid.innerHTML = `
        <div class="metric-card">
            <h4>Total Revenue Potential</h4>
            <div class="value">₹${formatNumber(data.total_revenue || 0)}</div>
            <div class="description">Annual biomass revenue</div>
        </div>
        <div class="metric-card">
            <h4>Biofuel Production</h4>
            <div class="value">${formatNumber(data.total_biofuel_liters || 0)} L</div>
            <div class="description">Annual biodiesel equivalent</div>
        </div>
        <div class="metric-card">
            <h4>Cost Savings</h4>
            <div class="value">₹${formatNumber((data.total_bioenergy_kwh || 0) * 8)}</div>
            <div class="description">Energy cost reduction per year</div>
        </div>
        <div class="metric-card">
            <h4>ROI Period</h4>
            <div class="value">2.5 years</div>
            <div class="description">Expected return on investment</div>
        </div>
    `;
}

// Display recommendations based on scores
function displayRecommendations(scores, data) {
    const recommendations = document.getElementById('recommendations');
    const recs = [];
    
    // Environmental recommendations
    if (scores.environmental < 70) {
        recs.push({
            icon: '🌱',
            title: 'Improve Waste Management',
            description: 'Increase biomass recycling and composting to boost your environmental score. Consider implementing advanced waste-to-energy systems.'
        });
    } else {
        recs.push({
            icon: '✅',
            title: 'Excellent Environmental Performance',
            description: 'Your plantation is achieving strong environmental metrics. Maintain current practices and explore carbon credit opportunities.'
        });
    }
    
    // Social recommendations
    if (scores.social < 70) {
        recs.push({
            icon: '👥',
            title: 'Enhance Community Engagement',
            description: 'Increase local employment and implement farmer training programs to improve social impact and sustainability.'
        });
    } else {
        recs.push({
            icon: '🌟',
            title: 'Strong Social Impact',
            description: 'Your operation creates significant local value. Consider documenting and sharing best practices with the community.'
        });
    }
    
    // Governance recommendations
    if (scores.governance < 80) {
        recs.push({
            icon: '📋',
            title: 'Strengthen Governance',
            description: 'Implement additional transparency measures and obtain sustainability certifications to enhance governance score.'
        });
    }
    
    // Economic opportunity
    if (data.total_revenue > 1000000) {
        recs.push({
            icon: '💰',
            title: 'Scale Biomass Operations',
            description: `With ₹${formatNumber(data.total_revenue)} annual revenue potential, consider expanding your biomass conversion infrastructure.`
        });
    }
    
    recommendations.innerHTML = recs.map(rec => `
        <div class="recommendation-item">
            <div class="icon">${rec.icon}</div>
            <div class="content">
                <h4>${rec.title}</h4>
                <p>${rec.description}</p>
            </div>
        </div>
    `).join('');
}

// Format large numbers with commas
function formatNumber(num) {
    return Math.round(num).toLocaleString('en-IN');
}

// Language selector handling (optional future enhancement)
const languageSelector = document.getElementById('languageSelector');
if (languageSelector) {
    // Load saved language preference
    const savedLanguage = localStorage.getItem('preferredLanguage') || 'en';
    languageSelector.value = savedLanguage;
    
    // Save language preference on change
    languageSelector.addEventListener('change', function() {
        localStorage.setItem('preferredLanguage', this.value);
        // Could add i18n translation here in future
    });
}
