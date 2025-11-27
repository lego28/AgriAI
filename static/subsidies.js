// All subsidies data from CSV
const subsidiesData = [
    // Central Government Schemes
    { state: "Central", crop: "General Agriculture", name: "PM-KISAN", details: "Direct income support of ₹6,000/year (3 installments) to all landholding farmers", agency: "Ministry of Agriculture", govType: "central", link: "https://pmkisan.gov.in/" },
    { state: "Central", crop: "Coconut", name: "Area Expansion Programme", details: "₹56,000/ha for planting; ₹45/seedling for new coconut plantation", agency: "Coconut Development Board", govType: "central", link: "http://coconutboard.gov.in/" },
    { state: "Central", crop: "Coconut", name: "Technology Mission on Coconut", details: "Support for productivity enhancement and value addition in coconut sector", agency: "Coconut Development Board", govType: "central", link: "http://coconutboard.gov.in/" },
    { state: "Central", crop: "Coconut", name: "MSP Support", details: "Minimum Support Price mechanism for coconut to ensure remunerative prices", agency: "Coconut Development Board", govType: "central", link: "http://coconutboard.gov.in/" },
    { state: "Central", crop: "Oil Palm", name: "NMEO-OP", details: "₹29,000/ha for planting; ₹12,000/ha maintenance for 5 years; Price assurance ₹14.40/kg FFB", agency: "Ministry of Agriculture", govType: "central", link: "https://nmoop.gov.in/" },
    { state: "Central", crop: "Oil Palm", name: "Viability Price Support", details: "Assured price of ₹14.40/kg for Fresh Fruit Bunches with 15.3% oil content", agency: "Ministry of Agriculture", govType: "central", link: "https://nmoop.gov.in/" },
    { state: "Central", crop: "Coffee", name: "ICDP Coffee", details: "50% subsidy (₹35,000/ha) for replanting old coffee gardens", agency: "Coffee Board", govType: "central", link: "https://www.indiacoffee.org/" },
    { state: "Central", crop: "Coffee", name: "Processing Equipment", details: "40-50% subsidy on coffee processing machinery and equipment", agency: "Coffee Board", govType: "central", link: "https://www.indiacoffee.org/" },
    { state: "Central", crop: "General Agriculture", name: "PM Kisan Maandhan", details: "Pension scheme for farmers aged 18-40: ₹3,000/month after 60 years", agency: "Ministry of Agriculture", govType: "central", link: "https://maandhan.in/" },
    { state: "Central", crop: "General Agriculture", name: "PM Fasal Bima Yojana", details: "Comprehensive crop insurance: 2% (Kharif), 1.5% (Rabi), 5% (Horticulture) premium", agency: "Ministry of Agriculture", govType: "central", link: "https://pmfby.gov.in/" },
    { state: "Central", crop: "General Agriculture", name: "KCC Interest Subvention", details: "Credit facility at 7% interest (4% with prompt repayment) for agricultural needs", agency: "Ministry of Agriculture", govType: "central", link: "https://pmkisan.gov.in/KCC.aspx" },
    { state: "Central", crop: "General Agriculture", name: "Fertilizer Subsidy", details: "Subsidized fertilizers through Direct Benefit Transfer to reduce input costs", agency: "Department of Fertilizers", govType: "central", link: "#" },
    { state: "Central", crop: "General Agriculture", name: "Soil Health Card", details: "Free soil testing and nutrient recommendations for optimal fertilizer use", agency: "Ministry of Agriculture", govType: "central", link: "https://soilhealth.dac.gov.in/" },
    { state: "Central", crop: "General Agriculture", name: "AIF", details: "Fund for infrastructure development in agriculture and allied sectors", agency: "Ministry of Agriculture", govType: "central", link: "#" },
    { state: "Central", crop: "General Agriculture", name: "PM-AASHA", details: "Price support scheme ensuring MSP for farmers through PSS/PDPS mechanisms", agency: "Ministry of Agriculture", govType: "central", link: "#" },
    { state: "Central", crop: "General Agriculture", name: "SMAM", details: "40-50% subsidy on farm machinery (up to ₹1.25 lakh); 50% for SC/ST/women", agency: "Ministry of Agriculture", govType: "central", link: "https://agrimachinery.nic.in/" },
    { state: "Central", crop: "General Agriculture", name: "FPO Formation", details: "₹18 lakh/FPO support for Farmer Producer Organizations formation and strengthening", agency: "Ministry of Agriculture", govType: "central", link: "#" },
    
    // State Government Schemes
    { state: "Kerala", crop: "Coconut", name: "State MIDH", details: "Additional state support for Mission for Integrated Development of Horticulture schemes", agency: "Kerala Agriculture Department", govType: "state", link: "#" },
    { state: "Kerala", crop: "General Agriculture", name: "Horticulture Support", details: "State-level financial assistance for horticulture crop development and promotion", agency: "Kerala Horticulture Department", govType: "state", link: "#" },
    { state: "Kerala", crop: "Coffee", name: "Tribal Coffee", details: "Special support for tribal farmers in coffee cultivation with enhanced subsidies", agency: "Kerala Tribal Development", govType: "state", link: "#" },
    { state: "Karnataka", crop: "Coconut", name: "Horticulture Grant", details: "State grants for coconut plantation development and productivity enhancement", agency: "Karnataka Horticulture Department", govType: "state", link: "#" },
    { state: "Karnataka", crop: "Coffee", name: "Coffee Allocation", details: "State allocation for coffee growers support and infrastructure development", agency: "Karnataka Coffee Board Office", govType: "state", link: "#" },
    { state: "Tamil Nadu", crop: "Coconut", name: "Horticulture", details: "Tamil Nadu state scheme for horticulture crops including coconut development", agency: "TN Horticulture Department", govType: "state", link: "#" },
    { state: "Tamil Nadu", crop: "General Agriculture", name: "Organic", details: "Support for organic farming adoption with certification and marketing assistance", agency: "TN Agriculture Department", govType: "state", link: "#" },
    { state: "Tamil Nadu", crop: "Coffee", name: "Tribal Support", details: "Special assistance for tribal coffee farmers in Nilgiris and other districts", agency: "TN Tribal Welfare", govType: "state", link: "#" },
    { state: "Andhra Pradesh", crop: "Oil Palm", name: "NFSM-Oil Palm", details: "National Food Security Mission allocation for oil palm cultivation in AP", agency: "AP Agriculture Department", govType: "state", link: "#" },
    { state: "Telangana", crop: "Oil Palm", name: "Oil Palm Mission", details: "State mission for oil palm expansion with enhanced support and buyback guarantee", agency: "Telangana Agriculture Department", govType: "state", link: "#" },
    { state: "Telangana", crop: "General Agriculture", name: "Rythu Bandhu", details: "Investment support of ₹10,000/acre/year (₹5,000 per season) for all landholding farmers", agency: "Telangana Agriculture Department", govType: "state", link: "#" },
    { state: "Assam", crop: "General Agriculture", name: "NHM-Assam", details: "National Horticulture Mission implementation in Assam with state co-funding", agency: "Assam Horticulture Department", govType: "state", link: "#" },
    { state: "Punjab", crop: "General Agriculture", name: "Free Electricity", details: "Free electricity for agricultural operations to reduce cultivation costs", agency: "Punjab Power Corporation", govType: "state", link: "#" },
    { state: "Odisha", crop: "General Agriculture", name: "RKVY Farm Ponds", details: "Support for farm pond construction under Rashtriya Krishi Vikas Yojana", agency: "Odisha Agriculture Department", govType: "state", link: "#" },
    { state: "Madhya Pradesh", crop: "General Agriculture", name: "RKVY Infrastructure", details: "Infrastructure development support for agricultural activities under RKVY", agency: "MP Agriculture Department", govType: "state", link: "#" },
    { state: "Maharashtra", crop: "General Agriculture", name: "Mahatma Jyotiba Phule Scheme", details: "State support for small and marginal farmers with various agricultural benefits", agency: "Maharashtra Agriculture Department", govType: "state", link: "#" }
];

// Create subsidy card HTML
function createSubsidyCard(subsidy) {
    const badgeClass = subsidy.govType === 'central' ? 'badge-central' : 'badge-state';
    const badgeText = subsidy.govType === 'central' ? 'Central Government' : 'State Government';
    
    return `
        <div class="subsidy-card" data-state="${subsidy.state}" data-crop="${subsidy.crop}" data-govtype="${subsidy.govType}">
            <div class="subsidy-header">
                <h3>${subsidy.name}</h3>
                <span class="badge ${badgeClass}">${badgeText}</span>
            </div>
            <div class="subsidy-body">
                <p class="subsidy-desc">${subsidy.details}</p>
                
                <div class="subsidy-details">
                    <div class="detail-item">
                        <strong>State:</strong>
                        <span>${subsidy.state}</span>
                    </div>
                    <div class="detail-item">
                        <strong>Crop:</strong>
                        <span>${subsidy.crop}</span>
                    </div>
                    <div class="detail-item">
                        <strong>Agency:</strong>
                        <span>${subsidy.agency}</span>
                    </div>
                </div>
                
                <div class="subsidy-footer">
                    ${subsidy.link && subsidy.link !== '#' ? `<a href="${subsidy.link}" target="_blank" class="btn btn-primary">Apply Now</a>` : '<span class="btn btn-secondary">Contact Local Office</span>'}
                </div>
            </div>
        </div>
    `;
}

// Load all subsidies
function loadSubsidies() {
    const container = document.getElementById('subsidiesContainer');
    if (!container) return;
    
    container.innerHTML = subsidiesData.map(subsidy => createSubsidyCard(subsidy)).join('');
}

// Filter subsidies
function applyFilters() {
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const govType = document.getElementById('govFilter')?.value || '';
    const state = document.getElementById('stateFilter')?.value || '';
    const crop = document.getElementById('cropFilter')?.value || '';
    
    const cards = document.querySelectorAll('.subsidy-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const cardGovType = card.getAttribute('data-govtype');
        const cardState = card.getAttribute('data-state');
        const cardCrop = card.getAttribute('data-crop');
        const cardText = card.textContent.toLowerCase();
        
        const matchesSearch = !searchTerm || cardText.includes(searchTerm);
        const matchesGov = !govType || cardGovType === govType;
        const matchesState = !state || cardState === state || (state === 'Central' && cardGovType === 'central');
        const matchesCrop = !crop || cardCrop === crop;
        
        if (matchesSearch && matchesGov && matchesState && matchesCrop) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide no results message
    const container = document.getElementById('subsidiesContainer');
    let noResultsMsg = document.getElementById('noResultsMsg');
    
    if (visibleCount === 0) {
        if (!noResultsMsg) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.id = 'noResultsMsg';
            noResultsMsg.style.gridColumn = '1 / -1';
            noResultsMsg.style.textAlign = 'center';
            noResultsMsg.style.padding = '3rem';
            noResultsMsg.style.color = 'var(--text-secondary)';
            noResultsMsg.innerHTML = '<h3>No subsidies found</h3><p>Try adjusting your filters or search terms</p>';
            container.appendChild(noResultsMsg);
        }
    } else {
        if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
}

// Clear all filters
function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('govFilter').value = '';
    document.getElementById('stateFilter').value = '';
    document.getElementById('cropFilter').value = '';
    applyFilters();
}

// Enhanced eligibility checker
function checkEligibility() {
    const state = document.getElementById('eligState')?.value;
    const crop = document.getElementById('eligCrop')?.value;
    const land = document.getElementById('eligLand')?.value;
    
    if (!state || !crop || !land) {
        alert('Please fill all fields to check eligibility');
        return;
    }
    
    const resultsDiv = document.getElementById('eligibilityResults');
    if (!resultsDiv) return;
    
    resultsDiv.innerHTML = '';
    resultsDiv.classList.add('show');
    
    // Filter eligible subsidies
    const eligible = subsidiesData.filter(subsidy => {
        // Central schemes available to all
        if (subsidy.govType === 'central') {
            // Check crop match
            if (subsidy.crop === 'General Agriculture') return true;
            if (subsidy.crop === crop) return true;
            return false;
        }
        
        // State schemes - must match state
        if (subsidy.state === state) {
            if (subsidy.crop === 'General Agriculture') return true;
            if (subsidy.crop === crop) return true;
            return false;
        }
        
        return false;
    });
    
    if (eligible.length === 0) {
        resultsDiv.innerHTML = '<div class="result-item"><h4>No schemes found</h4><p>Check your selection and try again</p></div>';
    } else {
        eligible.forEach(subsidy => {
            const item = document.createElement('div');
            item.className = 'result-item';
            item.innerHTML = `
                <h4>✓ ${subsidy.name}</h4>
                <p>${subsidy.details}</p>
                <small><strong>Agency:</strong> ${subsidy.agency}</small>
            `;
            resultsDiv.appendChild(item);
        });
    }
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Language switching
document.getElementById('languageSelector')?.addEventListener('change', function(e) {
    const lang = e.target.value;
    localStorage.setItem('preferredLanguage', lang);
    console.log('Language changed to:', lang);
});

// Initialize on page load
window.addEventListener('DOMContentLoaded', function() {
    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang) {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = savedLang;
        }
    }
    
    // Load all subsidies
    loadSubsidies();
    
    // Attach filter event listeners
    document.getElementById('searchInput')?.addEventListener('input', applyFilters);
    document.getElementById('govFilter')?.addEventListener('change', applyFilters);
    document.getElementById('stateFilter')?.addEventListener('change', applyFilters);
    document.getElementById('cropFilter')?.addEventListener('change', applyFilters);
    document.querySelector('.search-btn')?.addEventListener('click', applyFilters);
    document.getElementById('clearFilters')?.addEventListener('click', clearFilters);
});

// Make functions globally available
window.checkEligibility = checkEligibility;
