
 /* ==================== AGRIÀI AI APP ==================== */

let sessionId = null;
let currentCrop = 'coconut';
let chatHistory = [];
let isLoading = false;
let queryCount = 0;
let startTime = Date.now();

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Generate session ID
    generateSessionId();
    
    // Load chat history
    loadChatHistory();
    
    // Set default crop
    document.getElementById('cropType').value = currentCrop;
    updateInfoPanel();
    
    // Load saved language preference
    const savedLang = localStorage.getItem('preferredLanguage');
    const languageSelector = document.getElementById('languageSelector');
    if (savedLang && languageSelector) {
        languageSelector.value = savedLang;
    }
    
    // Listen to language changes
    if (languageSelector) {
        languageSelector.addEventListener('change', function(e) {
            localStorage.setItem('preferredLanguage', e.target.value);
            const langNames = {
                'en': 'English',
                'hi': 'Hindi (हिंदी)',
                'ta': 'Tamil (தமிழ்)',
                'te': 'Telugu (తెలుగు)'
            };
            console.log('Language changed to:', langNames[e.target.value]);
        });
    }
}

function setupEventListeners() {
    const messageInput = document.getElementById('messageInput');
    const messagesContainer = document.getElementById('messagesContainer');
    const scrollButton = document.getElementById('scrollButton');
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Enter to send (Shift+Enter for new line)
    messageInput.addEventListener('keydown', handleKeyPress);
    
    // Keyboard shortcut for voice input (Ctrl+M or Cmd+M)
    document.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'm') {
            event.preventDefault();
            startVoiceInput();
        }
    });
    
    // Show/hide scroll button on scroll
    messagesContainer.addEventListener('scroll', function() {
        const isNearBottom = this.scrollHeight - this.scrollTop - this.clientHeight < 200;
        if (isNearBottom) {
            scrollButton.classList.remove('show');
        } else {
            scrollButton.classList.add('show');
        }
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ==================== SESSION MANAGEMENT ====================

function generateSessionId() {
    return fetch('/generate_session', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            sessionId = data.session_id;
            updateInfoPanel();
        })
        .catch(err => console.error('Session error:', err));
}

function startNewChat() {
    // Generate new session ID
    generateSessionId().then(() => {
        // Clear chat
        chatHistory = [];
        document.getElementById('messagesContainer').innerHTML = `
        <div class="welcome-section">
            <div class="welcome-header">
                <h2>Welcome to AgriAI</h2>
                <p>Your AI-powered agricultural intelligence assistant</p>
            </div>
            
            <div class="quick-actions">
                <div class="action-grid">
                    <button class="action-card" onclick="quickAction('disease')">
                        <span class="action-icon">🦠</span>
                        <span class="action-text">Disease Detection</span>
                        <span class="action-desc">Identify crop diseases</span>
                    </button>
                    
                    <button class="action-card" onclick="quickAction('ripeness')">
                        <span class="action-icon">🍎</span>
                        <span class="action-text">Ripeness Check</span>
                        <span class="action-desc">Harvest timing</span>
                    </button>
                    
                    <button class="action-card" onclick="quickAction('yield')">
                        <span class="action-icon">📊</span>
                        <span class="action-text">Yield Analysis</span>
                        <span class="action-desc">Production forecast</span>
                    </button>
                    
                    <button class="action-card" onclick="quickAction('sustainability')">
                        <span class="action-icon">🌍</span>
                        <span class="action-text">ESG Scoring</span>
                        <span class="action-desc">Sustainability metrics</span>
                    </button>
                    
                    <button class="action-card" onclick="quickAction('biomass')">
                        <span class="action-icon">♻️</span>
                        <span class="action-text">Biomass Value</span>
                        <span class="action-desc">Circular economy</span>
                    </button>
                    
                    <button class="action-card" onclick="quickAction('knowledge')">
                        <span class="action-icon">📚</span>
                        <span class="action-text">Knowledge Base</span>
                        <span class="action-desc">Expert information</span>
                    </button>
                </div>
            </div>

            <div class="suggested-prompts">
                <p class="suggested-title">Try asking:</p>
                <button class="prompt-button" onclick="sendPrompt('My palm tree has rotting at the base')">
                    "My palm tree has rotting at the base"
                </button>
                <button class="prompt-button" onclick="sendPrompt('When should I harvest my coconut bunches?')">
                    "When should I harvest my coconut bunches?"
                </button>
                <button class="prompt-button" onclick="sendPrompt('Calculate biomass potential for 1000 palms')">
                    "Calculate biomass potential for 1000 palms"
                </button>
                <button class="prompt-button" onclick="sendPrompt('What is my plantation ESG score?')">
                    "What is my plantation ESG score?"
                </button>
            </div>
        </div>
    `;
        
        // Remove active state from history items
        document.querySelectorAll('.history-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Update info panel
        updateInfoPanel();
    });
}

// ==================== MESSAGE HANDLING ====================

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    input.value = '';
    input.style.height = 'auto';
    
    // Show loading
    showLoading();
    
    // Send to backend
    queryCount++;
    sendToBackend(message);
}

function sendPrompt(prompt) {
    document.getElementById('messageInput').value = prompt;
    sendMessage();
}

function quickAction(action) {
    const prompts = {
        'disease': 'Help me identify and diagnose diseases affecting my ' + currentCrop + ' crop',
        'ripeness': 'What are the ripeness stages and optimal harvest timing for ' + currentCrop + '?',
        'yield': 'Analyze and predict the yield potential for my plantation',
        'sustainability': 'Calculate ESG sustainability score and environmental impact',
        'biomass': 'Analyze biomass potential and circular economy opportunities',
        'knowledge': 'Tell me about best practices for ' + currentCrop + ' farming'
    };
    
    sendPrompt(prompts[action]);
}

function addMessageToChat(content, sender, metadata = {}) {
    // Remove welcome section if first message
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer.querySelector('.welcome-section')) {
        messagesContainer.innerHTML = '';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    // Create a wrapper for content and timestamp
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = formatContent(content);
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    
    messageWrapper.appendChild(contentDiv);
    messageWrapper.appendChild(timestamp);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageWrapper);
    
    messagesContainer.appendChild(messageDiv);
    
    // Smooth scroll to bottom
    scrollToBottom();
    
    chatHistory.push({ sender, content, timestamp: new Date() });
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    setTimeout(() => {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

function formatContent(content) {
    // Convert markdown-like formatting to HTML
    let html = content;
    
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
    
    // Code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Line breaks
    html = html.replace(/\n/g, '<br>');
    
    // Lists
    html = html.replace(/^• (.*)/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    html = html.replace(/^- (.*)/gm, '<li>$1</li>');
    
    return `<p>${html}</p>`;
}

function showLoading() {
    const messagesContainer = document.getElementById('messagesContainer');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai';
    loadingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content message-loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;
    loadingDiv.id = 'loadingMessage';
    messagesContainer.appendChild(loadingDiv);
    scrollToBottom();
}

function removeLoading() {
    const loadingMsg = document.getElementById('loadingMessage');
    if (loadingMsg) loadingMsg.remove();
}

// ==================== BACKEND COMMUNICATION ====================

async function sendToBackend(message) {
    try {
        isLoading = true;
        
        // Get selected language from the top navbar
        const languageSelector = document.getElementById('languageSelector');
        const selectedLanguage = languageSelector ? languageSelector.value : 'en';
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: message,
                crop_type: currentCrop,
                session_id: sessionId,
                language: selectedLanguage  // Send selected language
            })
        });
        
        const data = await response.json();
        removeLoading();
        
        // Format response based on crop type
        if (currentCrop === 'palm') {
            const aiMessage = formatPalmResponse(data);
            addMessageToChat(aiMessage, 'ai', data);
        } else {
            const aiMessage = data.response || 'No response available';
            addMessageToChat(aiMessage, 'ai', data);
        }
        
        // Reload chat history after sending message
        loadChatHistory();
        
    } catch (error) {
        console.error('Error:', error);
        removeLoading();
        addMessageToChat('Sorry, an error occurred. Please try again.', 'ai');
    } finally {
        isLoading = false;
    }
}

function formatPalmResponse(data) {
    let response = data.response || '';
    
    if (data.disease_detected) {
        response = `
**Disease Detected:** ${data.disease_detected}
**Confidence:** ${(data.confidence * 100).toFixed(1)}%

${response}
        `.trim();
    }
    
    return response;
}

// ==================== FILE UPLOAD ====================

function uploadImage() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // Show loading with crop-specific message
        showLoading();
        const cropNames = {
            'coconut': '🥥 Coconut',
            'palm': '🌴 Oil Palm',
            'coffee': '☕ Coffee',
            'rubber': '🌳 Rubber'
        };
        const cropName = cropNames[currentCrop] || 'Crop';
        addMessageToChat(`📷 Analyzing ${cropName} image with AI disease detector...`, 'system');
        
        // Convert to base64
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const imageData = event.target.result;
                
                // Show image preview
                const imagePreview = document.createElement('div');
                imagePreview.className = 'image-preview';
                imagePreview.innerHTML = `<img src="${imageData}" alt="Uploaded" style="max-width: 300px; border-radius: 8px;">`;
                const messagesContainer = document.getElementById('messagesContainer');
                messagesContainer.appendChild(imagePreview);
                scrollToBottom();
                
                // Send to backend for disease detection
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: 'Please analyze this image for diseases',
                        image_urls: [imageData],
                        crop_type: currentCrop,
                        session_id: sessionId,
                        language: document.getElementById('languageSelector')?.value || 'en'
                    })
                });
                
                const data = await response.json();
                removeLoading();
                
                // Enhanced response formatting
                let responseText = data.response;
                
                // Add disease detection badge if confident
                if (responseText.includes('Disease Detected:') || responseText.includes('disease')) {
                    responseText = '🔬 **Disease Detection Result**\n\n' + responseText;
                }
                
                addMessageToChat(responseText, 'ai', data);
                queryCount++;
                updateQuickStats();
                
            } catch (error) {
                console.error('Error:', error);
                removeLoading();
                addMessageToChat('⚠️ Error analyzing image. Please try again or check your internet connection.', 'ai');
            }
        };
        reader.readAsDataURL(file);
    };
    input.click();
}

// ==================== VOICE INPUT ====================

let recognition = null;
let isRecording = false;

function startVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    const messageInput = document.getElementById('messageInput');
    
    // Check if browser supports Speech Recognition
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('⚠️ Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        return;
    }
    
    // Toggle recording
    if (isRecording) {
        stopVoiceInput();
        return;
    }
    
    // Get language preference
    const languageSelector = document.getElementById('languageSelector');
    const selectedLang = languageSelector ? languageSelector.value : 'en';
    
    // Map language codes to Speech Recognition locale codes
    const langMap = {
        'en': 'en-IN',      // English (India)
        'hi': 'hi-IN',      // Hindi
        'ta': 'ta-IN',      // Tamil
        'te': 'te-IN'       // Telugu
    };
    
    // Initialize Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    
    recognition.lang = langMap[selectedLang] || 'en-IN';
    recognition.continuous = false;  // Stop after one result
    recognition.interimResults = true;  // Show partial results
    recognition.maxAlternatives = 1;
    
    // Visual feedback
    voiceBtn.style.backgroundColor = '#ef4444';
    voiceBtn.style.animation = 'pulse 1.5s infinite';
    voiceBtn.title = 'Recording... Click to stop';
    isRecording = true;
    
    // Add pulsing animation CSS if not exists
    if (!document.getElementById('voiceAnimationStyle')) {
        const style = document.createElement('style');
        style.id = 'voiceAnimationStyle';
        style.textContent = `
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.1); opacity: 0.8; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Handle speech results
    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Show interim results in textarea
        if (interimTranscript) {
            messageInput.value = interimTranscript;
            messageInput.style.fontStyle = 'italic';
            messageInput.style.opacity = '0.7';
        }
        
        // Set final transcript
        if (finalTranscript) {
            messageInput.value = finalTranscript.trim();
            messageInput.style.fontStyle = 'normal';
            messageInput.style.opacity = '1';
            
            // Show success feedback
            showNotification('✅ Voice captured successfully!', 'success');
        }
    };
    
    // Handle errors
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        const errorMessages = {
            'no-speech': '⚠️ No speech detected. Please try again.',
            'audio-capture': '⚠️ No microphone found or permission denied.',
            'not-allowed': '⚠️ Microphone access denied. Please allow microphone permissions.',
            'network': '⚠️ Network error. Check your internet connection.',
            'aborted': 'ℹ️ Recording stopped.'
        };
        
        const message = errorMessages[event.error] || `⚠️ Error: ${event.error}`;
        showNotification(message, 'error');
        
        stopVoiceInput();
    };
    
    // Handle end of recognition
    recognition.onend = () => {
        stopVoiceInput();
    };
    
    // Start recognition
    try {
        recognition.start();
        showNotification('🎤 Listening... Speak now!', 'info');
    } catch (error) {
        console.error('Failed to start recognition:', error);
        showNotification('⚠️ Failed to start voice input', 'error');
        stopVoiceInput();
    }
}

function stopVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    const messageInput = document.getElementById('messageInput');
    
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
    
    // Reset visual feedback
    voiceBtn.style.backgroundColor = '';
    voiceBtn.style.animation = '';
    voiceBtn.title = 'Voice Input';
    isRecording = false;
    
    messageInput.style.fontStyle = 'normal';
    messageInput.style.opacity = '1';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `voice-notification ${type}`;
    notification.textContent = message;
    
    // Add CSS for notification if not exists
    if (!document.getElementById('voiceNotificationStyle')) {
        const style = document.createElement('style');
        style.id = 'voiceNotificationStyle';
        style.textContent = `
            .voice-notification {
                position: fixed;
                top: 80px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideIn 0.3s ease-out;
            }
            
            .voice-notification.info {
                background: #3b82f6;
                color: white;
            }
            
            .voice-notification.success {
                background: #10b981;
                color: white;
            }
            
            .voice-notification.error {
                background: #ef4444;
                color: white;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add to body
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== CROP SWITCHING ====================

function switchCrop() {
    currentCrop = document.getElementById('cropType').value;
    
    // Update title
    const titles = {
        'coconut': '🥥 Coconut Assistant',
        'palm': '🌴 Oil Palm Assistant',
        'both': '🌍 Dual Crop Assistant'
    };
    
    document.getElementById('chatTitle').textContent = titles[currentCrop];
    updateInfoPanel();
}

// ==================== INFO PANEL ====================

function updateInfoPanel() {
    const cropInfo = {
        'coconut': 'Coconut (Cocos nucifera) - Tree of Life. Major regions: Kerala, Tamil Nadu, Karnataka. Cultivation: 2.2M hectares.',
        'palm': 'Oil Palm (Elaeis guineensis) - Biomass & biofuel potential. Ripeness stages: Green → Yellow → Red → Dark Red → Fallen.',
        'both': 'Dual-crop system supporting both Coconut and Oil Palm intelligence.'
    };
    
    document.getElementById('cropInfo').textContent = cropInfo[currentCrop];
    document.getElementById('sessionInfo').textContent = `Session: ${sessionId || 'Loading...'}`;
    
    updateQuickStats();
}

function updateQuickStats() {
    const elapsedTime = Math.floor((Date.now() - startTime) / 60000);
    document.getElementById('quickStats').innerHTML = `
        <li>Queries: ${queryCount}</li>
        <li>Messages: ${chatHistory.length}</li>
        <li>Time: ${elapsedTime}m</li>
    `;
}

function toggleInfoPanel() {
    // Toggle panel visibility
}

// ==================== SETTINGS & HELP ====================

function toggleSettings() {
    const modal = document.getElementById('settingsModal');
    modal.classList.toggle('hidden');
}

function closeSettings() {
    document.getElementById('settingsModal').classList.add('hidden');
}

function showHelp() {
    const modal = document.getElementById('helpModal');
    modal.classList.remove('hidden');
}

function closeHelp() {
    document.getElementById('helpModal').classList.add('hidden');
}

function changeTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
    }
}

// ==================== CHAT HISTORY ====================

function loadChatHistory() {
    // Load chat sessions from backend
    fetch('/get_chat_sessions')
        .then(res => res.json())
        .then(data => {
            const historyItems = document.getElementById('historyItems');
            if (!historyItems) return;
            
            if (data.sessions && data.sessions.length > 0) {
                historyItems.innerHTML = '';
                data.sessions.forEach(session => {
                    const item = document.createElement('div');
                    item.className = 'history-item';
                    if (session.session_id === sessionId) {
                        item.classList.add('active');
                    }
                    
                    const date = new Date(session.timestamp);
                    const timeStr = formatRelativeTime(date);
                    
                    item.innerHTML = `
                        <div class="history-item-content" onclick="loadSession('${session.session_id}')">
                            <div class="history-preview">${escapeHtml(session.preview)}</div>
                            <div class="history-meta">
                                <span>${timeStr}</span>
                                <span>${session.message_count} messages</span>
                            </div>
                        </div>
                        <button class="history-delete" onclick="deleteSession(event, '${session.session_id}')" title="Delete">🗑️</button>
                    `;
                    
                    historyItems.appendChild(item);
                });
            } else {
                historyItems.innerHTML = '<div class="history-empty">No chat history yet</div>';
            }
        })
        .catch(err => {
            console.error('Failed to load chat history:', err);
        });
}

async function loadSession(session_id) {
    try {
        const response = await fetch(`/get_chat_history/${session_id}`);
        const data = await response.json();
        
        if (data.messages && data.messages.length > 0) {
            // Clear current chat
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = '';
            
            // Set session ID
            sessionId = session_id;
            
            // Load messages
            data.messages.forEach(msg => {
                addMessageToChat(msg.user_message, 'user', { timestamp: new Date(msg.timestamp) });
                addMessageToChat(msg.ai_response, 'ai', { timestamp: new Date(msg.timestamp) });
            });
            
            // Update active state
            document.querySelectorAll('.history-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.closest('.history-item')?.classList.add('active');
            
            // Update info panel
            updateInfoPanel();
        }
    } catch (err) {
        console.error('Failed to load session:', err);
    }
}

async function deleteSession(event, session_id) {
    event.stopPropagation();
    
    if (!confirm('Delete this conversation?')) return;
    
    try {
        const response = await fetch(`/delete_chat_session/${session_id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        if (data.success) {
            // Reload history
            loadChatHistory();
            
            // If deleted current session, start new chat
            if (session_id === sessionId) {
                startNewChat();
            }
        }
    } catch (err) {
        console.error('Failed to delete session:', err);
    }
}

function formatRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 7) {
        return date.toLocaleDateString();
    } else if (days > 0) {
        return `${days}d ago`;
    } else if (hours > 0) {
        return `${hours}h ago`;
    } else if (minutes > 0) {
        return `${minutes}m ago`;
    } else {
        return 'Just now';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function saveChatHistory() {
    // Reload chat sessions list periodically
    loadChatHistory();
}

// Reload history every 30 seconds
setInterval(saveChatHistory, 30000);

// ==================== UTILITY FUNCTIONS ====================

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Update stats every minute
setInterval(updateQuickStats, 60000);

// Close modals on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.getElementById('settingsModal').classList.add('hidden');
        document.getElementById('helpModal').classList.add('hidden');
    }
});

// Close modals on outside click
document.addEventListener('click', (e) => {
    const settingsModal = document.getElementById('settingsModal');
    const helpModal = document.getElementById('helpModal');
    
    if (e.target === settingsModal) {
        settingsModal.classList.add('hidden');
    }
    if (e.target === helpModal) {
        helpModal.classList.add('hidden');
    }
});
