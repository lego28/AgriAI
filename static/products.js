// Sample product data
const products = [
    {
        id: 1,
        name: 'Hybrid Coconut Seedlings (Dwarf x Tall)',
        category: 'seeds',
        crop: 'coconut',
        price: 150,
        rating: 4.5,
        image: '🌱',
        desc: 'Premium hybrid coconut seedlings with high yield potential',
        details: [
            'Disease-resistant variety',
            'Starts bearing in 3-4 years',
            'Average yield: 80-100 nuts/year',
            'Height: 15-20 feet',
            'Certified by CDB'
        ]
    },
    {
        id: 2,
        name: 'Oil Palm Certified Seeds (Tenera)',
        category: 'seeds',
        crop: 'oil-palm',
        price: 250,
        rating: 4.8,
        image: '🌴',
        desc: 'High-quality Tenera variety oil palm seeds',
        details: [
            'FFB yield: 25-30 tons/ha/year',
            'Oil extraction rate: 20-22%',
            'Germination rate: >90%',
            'Certified by NMEO-OP',
            'Technical support included'
        ]
    },
    {
        id: 3,
        name: 'Arabica Coffee Plants (Premium)',
        category: 'seeds',
        crop: 'coffee',
        price: 120,
        rating: 4.6,
        image: '☕',
        desc: 'Premium Arabica coffee plants for tropical climate',
        details: [
            'Variety: Chandragiri, S.795',
            'Starts bearing in 3 years',
            'Suitable for elevation 1000-1500m',
            'Disease-resistant',
            'Coffee Board certified'
        ]
    },
    {
        id: 4,
        name: 'Organic NPK Fertilizer (20:10:10)',
        category: 'fertilizers',
        crop: 'general',
        price: 850,
        rating: 4.4,
        image: '🧪',
        desc: 'Balanced NPK fertilizer for all plantation crops - 50kg bag',
        details: [
            'Organic certified',
            'Slow-release formula',
            'Improves soil health',
            'Safe for environment',
            '50kg per bag'
        ]
    },
    {
        id: 5,
        name: 'Coconut Vermicompost Special',
        category: 'fertilizers',
        crop: 'coconut',
        price: 450,
        rating: 4.7,
        image: '🪱',
        desc: 'Enriched vermicompost for coconut palms - 25kg',
        details: [
            'Rich in micronutrients',
            'Improves water retention',
            'Increases nut size',
            'Organic & eco-friendly',
            'Ready to use'
        ]
    },
    {
        id: 6,
        name: 'Systemic Insecticide (Imidacloprid)',
        category: 'pesticides',
        crop: 'general',
        price: 320,
        rating: 4.3,
        image: '🛡️',
        desc: 'Effective against mealybugs, aphids, and borers - 500ml',
        details: [
            'Systemic action',
            'Long-lasting protection',
            'Safe when used as directed',
            'Dosage: 0.5ml/liter',
            'Approved by CIB&RC'
        ]
    },
    {
        id: 7,
        name: 'Organic Neem Oil Spray',
        category: 'pesticides',
        crop: 'general',
        price: 280,
        rating: 4.6,
        image: '🌿',
        desc: 'Natural pest control solution - 1 liter',
        details: [
            '100% organic',
            'Controls aphids, mites, whiteflies',
            'Safe for beneficial insects',
            'No residue',
            'Can be used till harvest'
        ]
    },
    {
        id: 8,
        name: 'Power Tiller (8 HP Diesel)',
        category: 'equipment',
        crop: 'general',
        price: 85000,
        rating: 4.5,
        image: '🚜',
        desc: 'Compact power tiller for small to medium farms',
        details: [
            '8 HP diesel engine',
            'Multi-purpose attachments',
            'Fuel-efficient',
            'Easy maintenance',
            'SMAM subsidy eligible'
        ]
    },
    {
        id: 9,
        name: 'Coconut De-husking Machine',
        category: 'equipment',
        crop: 'coconut',
        price: 35000,
        rating: 4.4,
        image: '🥥',
        desc: 'Electric coconut de-husking machine - 1000 nuts/hr',
        details: [
            'Capacity: 1000 nuts/hour',
            '2 HP motor',
            'Low power consumption',
            'Minimal maintenance',
            'Safety features included'
        ]
    },
    {
        id: 10,
        name: 'Coffee Pulping Machine (Manual)',
        category: 'processing',
        crop: 'coffee',
        price: 12000,
        rating: 4.2,
        image: '⚙️',
        desc: 'Manual coffee pulping machine for small growers',
        details: [
            'Capacity: 200kg/hr',
            'Cast iron construction',
            'Easy operation',
            'No electricity needed',
            'Adjustable settings'
        ]
    },
    {
        id: 11,
        name: 'Drip Irrigation Kit (1 Acre)',
        category: 'irrigation',
        crop: 'general',
        price: 45000,
        rating: 4.7,
        image: '💧',
        desc: 'Complete drip irrigation system for 1 acre',
        details: [
            'Saves 60% water',
            'Increases yield by 30-40%',
            'Complete kit with pump',
            'Easy installation',
            'PMKSY subsidy available'
        ]
    },
    {
        id: 12,
        name: 'Sprinkler Irrigation System',
        category: 'irrigation',
        crop: 'general',
        price: 32000,
        rating: 4.4,
        image: '🌊',
        desc: 'Portable sprinkler system for 0.5 acre',
        details: [
            'Covers 0.5 acre',
            'Adjustable spray pattern',
            'Portable design',
            'Weather-resistant',
            '1 year warranty'
        ]
    },
    {
        id: 13,
        name: 'Garden Pruning Shears (Professional)',
        category: 'tools',
        crop: 'general',
        price: 650,
        rating: 4.6,
        image: '✂️',
        desc: 'Heavy-duty pruning shears for coffee and coconut',
        details: [
            'Hardened steel blades',
            'Ergonomic handles',
            'Cuts up to 1 inch branches',
            'Rust-resistant',
            'Comfortable grip'
        ]
    },
    {
        id: 14,
        name: 'Coconut Harvesting Pole (Telescopic)',
        category: 'tools',
        crop: 'coconut',
        price: 3500,
        rating: 4.5,
        image: '🪝',
        desc: 'Telescopic harvesting pole - extends to 20 feet',
        details: [
            'Extends from 10-20 feet',
            'Lightweight aluminum',
            'Sharp cutting blade',
            'Safety lock mechanism',
            'Easy to operate'
        ]
    },
    {
        id: 15,
        name: 'Soil Testing Kit (Complete)',
        category: 'tools',
        crop: 'general',
        price: 2800,
        rating: 4.8,
        image: '🧪',
        desc: 'Complete soil testing kit with 100 tests',
        details: [
            'Tests pH, N, P, K',
            '100 tests included',
            'Easy to use',
            'Color chart included',
            'Portable case'
        ]
    },
    {
        id: 16,
        name: 'Electric Coconut Scraper',
        category: 'processing',
        crop: 'coconut',
        price: 8500,
        rating: 4.3,
        image: '🔪',
        desc: 'Electric coconut scraper for copra/oil extraction',
        details: [
            '0.5 HP motor',
            'Processes 50 coconuts/hr',
            'Stainless steel blades',
            'Easy cleaning',
            'Compact design'
        ]
    },
    {
        id: 17,
        name: 'FFB Mini Harvester (Oil Palm)',
        category: 'equipment',
        crop: 'oil-palm',
        price: 15000,
        rating: 4.5,
        image: '🔧',
        desc: 'Motorized FFB harvesting tool for oil palm',
        details: [
            'Petrol-powered',
            'Extends to 25 feet',
            'Vibration cutting mechanism',
            'Reduces labor by 70%',
            'Easy maintenance'
        ]
    },
    {
        id: 18,
        name: 'Weather Station (Smart Agriculture)',
        category: 'equipment',
        crop: 'general',
        price: 22000,
        rating: 4.7,
        image: '🌡️',
        desc: 'Smart weather station with mobile app',
        details: [
            'Temperature & humidity sensors',
            'Rainfall measurement',
            'Wind speed & direction',
            'Mobile app connectivity',
            'Solar powered'
        ]
    },
    {
        id: 19,
        name: 'Organic Potash Fertilizer',
        category: 'fertilizers',
        crop: 'coconut',
        price: 720,
        rating: 4.5,
        image: '💎',
        desc: 'High potash organic fertilizer for coconut - 25kg',
        details: [
            'K2O content: 12%',
            'Organic certified',
            'Improves nut quality',
            'Increases copra content',
            'Suitable for all soils'
        ]
    },
    {
        id: 20,
        name: 'Coffee Drying Trays (Set of 10)',
        category: 'processing',
        crop: 'coffee',
        price: 6500,
        rating: 4.4,
        image: '☀️',
        desc: 'Mesh drying trays for coffee beans - set of 10',
        details: [
            'Food-grade mesh',
            'Stackable design',
            'Weather-resistant',
            '3ft x 2ft size',
            'Aluminum frame'
        ]
    }
];

let filteredProducts = [...products];

// Language switching
document.getElementById('languageSelector')?.addEventListener('change', function(e) {
    const lang = e.target.value;
    localStorage.setItem('preferredLanguage', lang);
    console.log('Language changed to:', lang);
});

// Load saved language preference
window.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang) {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = savedLang;
        }
    }
    
    // Load products on page load
    displayProducts(products);
});

// Display products
function displayProducts(productsToShow) {
    const container = document.getElementById('productsContainer');
    const noResults = document.getElementById('noResults');
    
    if (productsToShow.length === 0) {
        container.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    container.innerHTML = '';
    
    productsToShow.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.onclick = () => showProductDetails(product);
        
        card.innerHTML = `
            <div class="product-image">${product.image}</div>
            <div class="product-info">
                <div class="product-category">${getCategoryName(product.category)}</div>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-desc">${product.desc}</p>
                <div class="product-meta">
                    <span class="product-price">₹${product.price.toLocaleString()}</span>
                    <span class="product-rating">
                        <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                        ${product.rating}
                    </span>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Get category display name
function getCategoryName(category) {
    const names = {
        'seeds': 'Seeds & Seedlings',
        'fertilizers': 'Fertilizers',
        'pesticides': 'Pesticides',
        'equipment': 'Equipment',
        'irrigation': 'Irrigation',
        'tools': 'Tools',
        'processing': 'Processing'
    };
    return names[category] || category;
}

// Filter products
function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    const crop = document.getElementById('cropFilter').value;
    const priceRange = document.getElementById('priceFilter').value;
    
    filteredProducts = products.filter(product => {
        // Search filter
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) || 
                             product.desc.toLowerCase().includes(searchTerm);
        
        // Category filter
        const matchesCategory = !category || product.category === category;
        
        // Crop filter
        const matchesCrop = !crop || product.crop === crop || product.crop === 'general';
        
        // Price filter
        let matchesPrice = true;
        if (priceRange) {
            if (priceRange === '0-1000') {
                matchesPrice = product.price <= 1000;
            } else if (priceRange === '1000-5000') {
                matchesPrice = product.price > 1000 && product.price <= 5000;
            } else if (priceRange === '5000-25000') {
                matchesPrice = product.price > 5000 && product.price <= 25000;
            } else if (priceRange === '25000+') {
                matchesPrice = product.price > 25000;
            }
        }
        
        return matchesSearch && matchesCategory && matchesCrop && matchesPrice;
    });
    
    displayProducts(filteredProducts);
}

// Search products
function searchProducts() {
    filterProducts();
}

// Clear filters
function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('categoryFilter').value = '';
    document.getElementById('cropFilter').value = '';
    document.getElementById('priceFilter').value = '';
    displayProducts(products);
}

// Attach event listeners
document.getElementById('searchInput')?.addEventListener('input', filterProducts);
document.getElementById('categoryFilter')?.addEventListener('change', filterProducts);
document.getElementById('cropFilter')?.addEventListener('change', filterProducts);
document.getElementById('priceFilter')?.addEventListener('change', filterProducts);

// Show product details in modal
function showProductDetails(product) {
    const modal = document.getElementById('productModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <div class="modal-product-image">${product.image}</div>
        <h2 class="modal-product-name">${product.name}</h2>
        <div class="product-rating">
            <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
            ${product.rating} / 5.0
        </div>
        <div class="modal-product-price">₹${product.price.toLocaleString()}</div>
        <p class="modal-product-desc">${product.desc}</p>
        
        <div class="modal-product-details">
            <h3>Product Details</h3>
            <ul>
                ${product.details.map(detail => `<li>${detail}</li>`).join('')}
            </ul>
        </div>
        
        <div class="modal-actions">
            <button class="btn btn-primary" onclick="contactSeller('${product.name}')">Contact Seller</button>
            <button class="btn btn-secondary" onclick="addToWishlist(${product.id})">Add to Wishlist</button>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('productModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Contact seller (placeholder)
function contactSeller(productName) {
    alert(`To purchase "${productName}", please contact:\n\n📞 Customer Care: 1800-XXX-XXXX\n📧 Email: support@agriai.com\n\nOr visit your nearest agricultural supply store.`);
}

// Add to wishlist (placeholder)
function addToWishlist(productId) {
    alert('Product added to wishlist!\n\nNote: This is a demo feature.');
    console.log('Added to wishlist:', productId);
}

// Make functions globally available
window.searchProducts = searchProducts;
window.clearFilters = clearFilters;
window.closeModal = closeModal;
window.showProductDetails = showProductDetails;
